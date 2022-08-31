import copy
import os

import numpy as np

from hexrd.config.root import RootConfig
from hexrd.config.material import MaterialConfig
from hexrd.config.instrument import Instrument as InstrumentConfig

from hexrd.ui.create_hedm_instrument import create_hedm_instrument
from hexrd.ui.hexrd_config import HexrdConfig


def get_indexing_material():
    indexing_config = HexrdConfig().indexing_config
    available_materials = list(HexrdConfig().materials)
    selected_material = indexing_config.get('_selected_material')

    if selected_material not in available_materials:
        raise Exception(f'Selected material {selected_material} not available')

    return HexrdConfig().material(selected_material)


def create_indexing_config():
    # Creates a hexrd.config class from the indexing configuration

    material = get_indexing_material()
    pd = material.planeData

    # Make a copy to modify
    indexing_config = copy.deepcopy(HexrdConfig().indexing_config)

    # Set the active material on the config
    tmp = indexing_config.setdefault('material', {})
    tmp['active'] = material.name

    # Create the root config from the indexing config dict
    config = RootConfig(indexing_config)

    # Create and set instrument config
    iconfig = InstrumentConfig(config)
    iconfig._hedm = create_hedm_instrument()
    config.instrument = iconfig

    # Create and set material config
    mconfig = MaterialConfig(config)
    mconfig.materials = HexrdConfig().materials
    config.material = mconfig

    # Set this so the config won't over-write our tThWidth
    config.set('material:tth_width', np.degrees(material.planeData.tThWidth))

    ims_dict = HexrdConfig().omega_imageseries_dict
    if ims_dict is None:
        # Add an early error that is easier to understand...
        raise OmegasNotFoundError('Omegas not found!')

    config.image_series = ims_dict

    validate_config(config)

    return config


def validate_config(config):
    # Perform any modifications to make sure this is a valid config
    try:
        config.working_dir
    except IOError:
        # This working directory does not exist. Set it to the cwd.
        print(f'Warning: {config.get("working_dir")} does not exist.',
              f'Changing working directory to {os.getcwd()}')
        config.set('working_dir', os.getcwd())

        # Make sure future configs use the new working dir as well...
        HexrdConfig().indexing_config['working_dir'] = os.getcwd()


class OmegasNotFoundError(Exception):
    pass
