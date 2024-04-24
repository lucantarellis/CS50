-- FIRST: Get the license plate of the car.(3.txt)
SELECT
    hour,
    minute,
    activity,
    license_plate
FROM bakery_security_logs
WHERE activity = 'exit' AND day = 28 AND month = 07 AND year = 2021;
-- I need more information about the exact time to get the correct license plate.
-- SECOND: Get more info about that "less than a minute" phone call.(4.txt)
SELECT
    caller,
    receiver,
    duration
FROM phone_calls
WHERE duration < 60 AND day = 28 AND month = 07 AND year = 2021;
-- Got some suspects but I need more information.
-- THIRD: I'll look for information about the ATM usage.(5.txt)
SELECT
    account_number,
    amount
FROM atm_transactions
WHERE atm_location = 'Leggett Street' AND transaction_type = 'withdraw' AND day = 28 AND month = 07 AND year = 2021;
-- OK I have some account numbers and telephones that coud lead to our suspect. I'll go and check the flights (6.txt)
SELECT
    f.id,
    f.hour,
    f.minute,
    a1.city AS "From",
    a2.city AS "To"
FROM flights AS f
JOIN airports AS a1 ON a1.id = f.origin_airport_id
JOIN airports AS a2 ON a2.id = f.destination_airport_id
WHERE f.day = 29 AND f.month = 07 AND f.year = 2021
ORDER BY f.hour;
-- OK, now I have five flights that departs from Fiftyville, the first one is at 8:20 AM to NYC with ID 36. Now I'll try to match the ID of the flights that departs from Fiftyville with the passports and licence plates. (7.txt)
SELECT
    flight_id,
    passport_number,
    seat
FROM passengers
WHERE flight_id = 36;
-- With this information I'll go and match the passports number with each person (8.txt)
SELECT
    id,
    name,
    phone_number,
    passport_number,
    license_plate
FROM people
WHERE passport_number = 7214083635 OR passport_number = 1695452385 OR passport_number = 5773159633 OR passport_number = 1540955065 OR passport_number = 8294398571 OR passport_number = 1988161715 OR passport_number = 9878712108 OR passport_number = 8496433585;
-- I have two passengers that match with the phone call that lasted less than one minute BUT there's no license plate that match with the car that exited the bakery on that day.
-- I'll try to find out more information about the bank accounts of these two suspects; Kenny with ID 395717 and Doris with ID 953679 (9.txt)
SELECT
    person_id,
    account_number,
    creation_year
FROM bank_accounts
WHERE person_id = 953679 OR person_id = 395717;
-- To make things right I'm going to match the only account number that I got from the last query (Kenny's account number) and match it with the atm_transactions (10.txt)
SELECT *
FROM atm_transactions
WHERE account_number = 28296815 AND day = 28 AND month = 07 AND year = 2021;
-- The only person that has a bank account is Kenny, the same account that withdrew money from Leggett Street the day of the robbery. So we can confirm Kenny is the THIEF, Doris the ACCOMPLICE and they ESCAPED to New York City.



SELECT
    f.id,
    f.hour,
    f.minute,
    a1.city,
    a2.city
FROM flights AS f
JOIN airports AS a1 ON a1.city = f.origin_airport_id
JOIN airports AS a2 ON a2.city = f.destination_airport_id
WHERE f.day = 28 AND f.month = 07 AND f.year = 2021;

SELECT
    m.id,
    u1.username,
    u2.username,
    m.text
FROM
    messages AS m
INNER JOIN
    users AS u1 ON u1.id = m.from
INNER JOIN
    users AS u2 ON u2.id = m.to