# Installation

- ensure you have pipenv installed, and python running 3.10.5
- pipenv install

# Architecture notes

## models:

### Accounts
- User (customer)
- - 

- Vehicle
- - FK to user, null=True, blank=True
- - license plate
- - model, null=True, blank=True
- - type, null=True, blank=True

### Sessions
- ParkingLot
- - code
- - floor

- Session
- - FK to Vehicle
- - FK to ParkingLot
- - FK to Price
- - type (reservation, spot)
- - start datetime
- - end datetime
- - check_in
- - check_out
- - active

- Rates
- - name (free, discount, standard, premium)
- - value (0.00, 2.00, 4.00)

- Time Periods
- - from time
- - to time

- Payment
- - status (not started, pending, declined, completed)


# Full-stack developer Candidate

## Assignment

The first part of this assignment is the most important, answering the last would give you an
advantage. For ANY questions, please feel free to contact us about it.
The assignment should be completed within a week but if you need more time, let us know.

### Part one
This assignment is quite open for interpretation, however, this was done on purpose. We’d like
to see how you would approach such a project and expect an end result that matches with the
vacancy you are applying for. We’d like to see your train of thought about the architecture and
which aspects of the problem we lined out below you considered, but left out on purpose and
which assumptions you made. Also think about adding tests and such.

The story of a parking lot attend
Bob is a parking lot attend. The lot he works at does not have any automation which means
it's Bob's responsibility to ensure the integrity of the lot. In this parking lot, people prepay for
spots for a specific amount of time. People are also able to make reservations in advance
to ensure there will be a parking spot available for them when they arrive. At the current
moment whenever a new user comes to the lot without a reservation it's Bob's job to go
around the lots to ensure that there is still a spot available and that this new car does not
overlap the reservation of someone coming later in the day or week (or year...). Bob believes
that there is a way to automate this process by building a webapp that handles parking
reservations and can show the occupation rate of the parking lot so it can quickly determine
whether there is a spot available for any time a user chooses, or not.
Your challenge:
● Build a webapp that accomplishes the requirements outlined in the story
● This should be a demo program that can be run and used as a proof of concept
● There should be clear documentation that explains how to run and use the program
as well as future ideas for how to improve it,
● We're always happy to be surprised and see your approach to this problem
● We use Docker, Django, and Python and react.js in the company however feel free to use
other tools and languages if you feel they are better suited to this problem

### Part two
One of the applications we are currently running consists of a frontend server (Ridesharing) and
backend server (Travel matrix). Both systems are comprised of multiple dockers, combined into
microservices, and several databases. The api service consists of a django based rest
framework combined with a postgres backend running behind a Kong API gateway interface.
This platform, thus primarily running as an API service, must be made ready for horizontal
(auto)scaling and become redundant (double servers if you will) in its setup for continuity
reasons as well as rolling application updates during the day.
Your challenge:
- Deliver a design of a possible end setup, as well as a plan of attack to get there.
- What technologies would you choose to realise this and why?
- What questions would you like to have seen answered upfront to have delivered an even
better design?