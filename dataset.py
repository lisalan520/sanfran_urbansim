import pandas as pd
import assumptions
import utils
import urbansim.sim.simulation as sim

import warnings
warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)


@sim.table_source('jobs')
def jobs(store):
    df = store['jobs']
    df = utils.fill_nas_from_config('jobs', df)
    return df


@sim.table_source('buildings')
def buildings(store):
    df = store['buildings']
    df = df[df.building_type_id > 0]
    df = df[df.building_type_id <= 14]
    df["residential_sales_price"] = 0
    df["non_residential_rent"] = 0
    df = utils.fill_nas_from_config('buildings', df)
    return df


@sim.table_source('households')
def households(store):
    df = store['households']
    return df


@sim.table_source('parcels')
def parcels(store):
    df = store['parcels']
    return df


# these are shapes - "zones" in the bay area
@sim.table_source('zones')
def zones(store):
    df = store['zones']
    return df


# starts with the same underlying shapefile, but is used later in the simulation
@sim.table_source('zones_prices')
def zones_prices(store):
    df = store['zones']
    return df


# this is the mapping of parcels to zoning attributes
@sim.table_source('zoning_for_parcels')
def zoning_for_parcels(store):
    df = store['zoning_for_parcels']
    df = df.reset_index().drop_duplicates(cols='parcel').set_index('parcel')
    return df


# this is the actual zoning
@sim.table_source('zoning')
def zoning(store):
    df = store['zoning']
    return df


# zoning for use in the "baseline" scenario
# comes in the hdf5
@sim.table_source('zoning_baseline')
def zoning_baseline(zoning, zoning_for_parcels):
    df = pd.merge(zoning_for_parcels.to_frame(),
                  zoning.to_frame(),
                  left_on='zoning',
                  right_index=True)
    return df


sim.broadcast('zones', 'homesales', cast_index=True, onto_on='zone_id')
sim.broadcast('zones', 'costar', cast_index=True, onto_on='zone_id')
sim.broadcast('zones', 'apartments', cast_index=True, onto_on='zone_id')
sim.broadcast('zones', 'buildings', cast_index=True, onto_on='zone_id')
sim.broadcast('zones_prices', 'buildings', cast_index=True, onto_on='zone_id')
sim.broadcast('parcels', 'buildings', cast_index=True, onto_on='parcel_id')
sim.broadcast('buildings', 'households', cast_index=True, onto_on='building_id')
sim.broadcast('buildings', 'jobs', cast_index=True, onto_on='building_id')
