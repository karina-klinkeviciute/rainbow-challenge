# The strucure of the project

Project consists of these parts:
1. [Challenges](challenges.md)
2. [Joined challenges](challenges.md) - each Challenge has its counterpart joined challenge.
   They are used for storing the data for that challenge for each user that joins the challenge.
   Joining challenges with endpoints is explained [here](challenge_actions.md)
3. User - stores all the information about the user. Also has methods for displaying calculated information about
    the activity of the user.
4. Results. This is further divided into the following:
   1. Regions. They are not a part of results themselves, but they are used in calculating results per region.
   2. Streak. Calculation of weekly streaks. Users get +1 streak each week in a row if they complete at least one challenge and -1 if they don't.
   3. Medal. Medals are connected to streaks. Users receive medals after they complete 10, 20, 30, 40 streaks. 
   4. Prize. Prizes are shown in the Prize "shop" and can be claimed by users. Users earn Rainbows by completing challenges and later can exchange those Rainbows into prizes.
5. Quiz. It's a type of challenge but for its complexity and also because its potential to be used as a single app, it has been moved to a separate django app. 
6. Messaging. Messaging will only be happening between a user and admins, not between users. The same system will also be used for in-app notifications. 

## Challenges

Challenges is the main part of the app. 

Types of challenges:

* article
* custom
* organizing an event
* participating in an event
* project
* quiz
* reacting to public events
* telling your story
* support
* School GSA

