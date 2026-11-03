# Addressing Standards

Address standards serve different purposes. The application needs a flexible
international representation for postal and physical addresses, while financial
messaging schemas may impose a more specific structure on addresses embedded in
payments.

## UPU S42

UPU S42 provides a generic set of postal address elements and country-specific
templates. The elements cover organization and department, premises, thoroughfare,
locality, postcode, post box, and country. Its purpose is to support postal address
formats across countries.

The project notes recommend using S42 as a reference for an international address
model, with country-specific formatting applied when displaying or preparing an
address for delivery.

## ISO 20022

ISO 20022 is a financial messaging standard. Its postal-address structures provide
fields used when address data is exchanged in financial messages; they are not a
replacement for a general-purpose international postal address model.

Relevant structured elements include department, sub-department, street name,
building number/name, floor, post box, room, postal code, town, district, country
subdivision, country, and optional address lines. Supported fields depend on the
specific ISO 20022 message and schema version.

## Design guidance

- Keep address components structured; do not make a single formatted string the only
  stored representation.
- Preserve the country and source format, and apply country-specific presentation
  rules when rendering.
- Distinguish postal addresses from physical/geographic locations.
- Do not assume one standard's fields map losslessly to another standard's schema.
- Confirm the target message/version before producing ISO 20022 address payloads.

For the app's current UK field example, see [[uk-address-format]].
