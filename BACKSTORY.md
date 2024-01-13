# Backstory
This project was created as part of one of my University courses.
The goal of the course was to integrate AI solution into a bot playing StarCraft II.

The project you see here was my contribution. A bayesian model that tries to predict the outcome should two armies battle.
Not much more to say really. The model itself is based on [this](https://ojs.aaai.org/index.php/AIIDE/article/view/12683) (great) paper.
Due to time constraints several concessions were made. No nodes are continuous, for example.

Simulation data was created using [sc2combatsim](https://github.com/jgs03177/sc2combatsim/). Great tool, a bit hard to configure.

#### Does the model work?

Yes.

#### Does it work well?

Not at all. It's quite horrible acutally.

The main problem lies in the fact that nodes are discretized.
Whilst I'm in no way sure, I'm fairly confident that it would at least be useable if this were not the case.
The aforementioned paper shows that good results are possible in SC1. I find it hard to believe that wouldn't carry over to SC2.

On top of this `MLE` as a prameter estimation method tends to overly adapt the model to the training data.
Some other method should definitely be used. 

#### Is good at anything?

It's okay fast to make predictions. Usually well within the frame time budget we had in the SC2 bot.

#### Is there a full paper about this?

Yes.

#### Is it written in Swedish?

Also yes.

#### Will it be available?

Probably not - here's why:
1. There's no way I'm translating it.
2. The scope is broader that this code project. Most of it is just not very relevant here.


Peace, love, and hail Satan.

// Oskar
