select 
  property_id,
  address,
  max(`core.opa_assessments`.year),
  market_value,
  any_value(geog) as geog,
  from 
`core.pwd_parcels` join `core.opa_assessments`
on `core.pwd_parcels`.property_id = `core.opa_assessments`.parcel_number
group by property_id, address, market_value
LIMIT 10;