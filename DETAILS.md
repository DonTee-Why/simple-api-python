# Simple-Api-Python

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Design

This is a simple API written in python. The features of this API are:

  - A `GET /howold` endpoint.
  - Calculate and return the age of a person, given the date of birth (dob), in timestamp format, passed as query parameters to the GET/howold endpoint.
  - Limits calls to the endpoint to allow a maimum of 3 calls per second.
  - Return the right HTTP error if the date of birth parameter (dob) is not properly used or if the value is invalid

## How does this work

This API was implemented using a python framework called [FastAPI](https://fastapi.tiangolo.com/). When a request is made to the `/howold` endpoint, it first hits the `main.py` file. It then gets to the `endpoints.py` file which contains the function implementation for the endpoint. The function then accepts the parameter passed to the endpoint, performs operations like rate limiting and other necessary checks and then returns the appropriate response.

### Files

#### `main.py`

This is the main entry point of the program. In this file the FastAPI app is created.

#### `src/endpoints.py`

This file contains the `GET /howold` endpoint function. The function accepts a parameter `dob` (date of birth). In this function, the rate limiter is first used to monitor the number of requests handled within a period of time. If the rate limiter flags too many requests, a 429 error (Too Many Requests) is returned.

Some checks are then done on the `dob` parameter. The parameter is then checked if it is setor null. This returns the 422 code (Unprocessable Entity).

The next thing is to convert `dob` parameter to a valid Python `datetime` object. This conversion handles negative timestamp which represents dates before the UNIX Epoch (January 1st, 1970 at 00:00:00 UTC). If the parameter is not a valid timestamp, it throws an exception and returns the 422 code (Unprocessable Entity).

The next check is then performed to ensure that the provided date of birth is not in the future. This check returns a 400 code (Invalid Input).

The age is then calculated using the date of birth and the current date. The fact that days and months in the future means that a birthday year cycle is not complete yet is also factored in the calculation. This is done by deducting the age (initially calculated using the date of birth and the current date) by 1 if the day or month is in the future and by 0 if otherwise.

#### `src/rate_limiter.py`

This is where the the rate limiter function is implemented. Thes function accepts the following parameters:

  - **Key** as a String: The IP address of the user
  - **Limit** as an Integer: The number of requests allowed within a period of time
  - **Period** in Seconds: The period of time a certain number of requests are allowed

The rate limiter uses the token bucket algorithm. This implementation make use of [Redis](https://redis.io/) for cache to store information regarding requests. Redis cache provides a key-value store. The rate limiter works as follows:

  - A Redis key-value pair record is created where the key is the user's IP address and the value is the limit. If the record exists, it is set to   expire in the specified period.
  - When a request is made, if the limit is not used up (i.e not equal to zero), it is processed. Otherwise, the request is denied.
  - When a request is processed, the limit is reduced.
  - After the period has elapsed, the limit is then set to its original value.
