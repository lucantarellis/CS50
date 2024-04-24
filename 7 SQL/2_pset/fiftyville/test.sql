SELECT
    p.name,
    p.phone_number,
    p.passport_number,
    p.license_plate,
    ba.account_number
FROM passengers pa
JOIN people p ON p.passport_number = pa.passport_number
JOIN flights f ON f.id = pa.flight_id
JOIN bank_accounts ba ON ba.person_id = p.id
WHERE f.id = 36;