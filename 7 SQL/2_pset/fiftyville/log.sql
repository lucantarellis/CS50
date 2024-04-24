-- Keep a log of any SQL queries you execute as you solve the mystery.

-- All I know is that the theft took place on July 28, 2021 and that it took place on Humphrey Street.
-- I'll start by looking the crime_scene_reports table, let's see if I can find out something about the date the duck was stolen.
SELECT
    day,
    month,
    year,
    description
FROM crime_scene_reports
WHERE street = 'Humphrey Street';
-- Robbery was at 10:15 AM, three people witnessed it. Let's find out.
SELECT
    name,
    transcript
FROM interviews
WHERE transcript LIKE '%bakery%' AND day = 28 AND month = 07 AND year = 2021;
-- Witness 1: Sometime within ten minutes after the theft, someone saw the thief exit the bakery parking lot and drive away. There might be some security camera's footage.
SELECT
    p.name,
    bsl.license_plate,
    bsl.activity
FROM bakery_security_logs bsl
JOIN people p ON p.license_plate = bsl.license_plate
WHERE bsl.day = 28 AND bsl.month = 07 AND bsl.year = 2021 AND hour = 10 AND minute BETWEEN 15 AND 25;
-- Witness 2: The perk was seen using the ATM located on Leggett Street the same day of the robbery.
SELECT
    p.name,
    at.account_number
FROM atm_transactions at
JOIN bank_accounts ba ON ba.account_number = at.account_number
JOIN people p ON p.id = ba.person_id
WHERE at.atm_location = 'Leggett Street' AND at.day = 28 AND at.month = 07 AND at.year = 2021 AND transaction_type = 'withdraw';
-- Witness 3: The thief spoke with someone else for less than a minute. They were going to buy the earliest flight ticket available on the next morning (29/07/2023).
SELECT
    c.name AS "Caller",
    pc.caller,
    r.name AS "Receiver",
    pc.receiver,
    pc.duration
FROM phone_calls pc
JOIN people c ON c.phone_number = pc.caller
JOIN people r ON r.phone_number = pc.receiver
WHERE pc.day = 28 AND pc.month = 07 AND pc.year = 2021 AND pc.duration < 60;
-- Follow up: I'll try to find out more about the flight in the next morning.
SELECT
    f.id,
    f.hour,
    f.minute,
    a.city AS "Origin",
    b.city AS "Destination"
FROM flights f
JOIN airports a ON a.id = origin_airport_id
JOIN airports b ON b.id = destination_airport_id
WHERE f.day = 29 AND f.month = 07 AND f.year = 2021
ORDER BY f.hour ASC;
-- I'll match the first flight to New York City (id = 36) with the information about the passengers to find out who is the thief.
SELECT
    p.name,
    p.phone_number,
    p.passport_number,
    p.license_plate
FROM passengers pa
JOIN people p ON p.passport_number = pa.passport_number
JOIN flights f ON f.id = pa.flight_id
WHERE f.id = 36;
-- If I add the bank account on those passengers, the list shortens to 4 suspects.
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
-- Now I'll mix the information gathered. We can first discard Kenny, as he did not exit the bakery on the day of the robery. The same is true with Taylor. We can also discard Luca since he did not call anyone on the day of the robbery.
-- So we are left with Bruce, we can confirm he is the thief and Robin is the accomplice.