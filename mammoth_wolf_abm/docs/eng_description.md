<h1>Rabbits, Grass and Weeds population model<br>
<img src="rabbitgrassweed/pics/frabbit.png">
<img src="rabbitgrassweed/pics/rabbit.png"></h1>

<h2>Introduction</h2>

The "Rabbits, Grass and Weed" is a self-programmed mesa implementation and extension of an agent-based model created in NetLogo.
This model models the cohabitation of a herbivorous species and two of its foods.
The default model type is meant to implement the original model as faithfully as possible while in the "Extended model" type the animals have genders.<br>

This kind of model can primarily be utilized in the fields of agriculture and nature conservation. Within agriculture it can be useful for planning animal husbandry while within nature conservation the effects of intervention for the preservation of the endangered species can be simulated. Naturally, this exact model cannot be applied for either use cases since it's primitive but it can serve as a starting point instead. The model in its current form can be mostly used for presentation.<br>

<br><h2>The model types' operational characteristics</h2>

<h3>Mutual characteristics</h3>

In both model types, there is a herbivorous species, which is represented by rabbits.
These rabbits live in such an area where grass and weeds can grow randomly and have a set nutritional value.
Furthermore, all entities have some energy (energy point or EP for short from now on) which is decreased by one in every step (the model's change of state) but is increased by a given parameter based on the food type by eating. If their energy is fully consumed, they die. They can also reproduce if their EP is above a set threshold, however doing so halves their energy. During one step of the model, the animal agents move to one of the neighboring cells where the neighbors are the Moore-neighbors excluding the agent's current cell so they can't stay still.<br>

About the energy point it is worth noting that the program uses one less EP than what can be seen on an animal in the visualization application if the cursor is on it. This is meant to adjust that the reproduction threshold and intial maximal EP parameters work with strict inequality. These parameters' sliders can be set according to the displayed values. So the application displays at least 1 EP for the user. Pointing the cursor at an animal also displays a "Layer: 1" value which cannot be got rid of. For the grass agents the layer is 0 which hides this pop up on them but not on the animals.<br>

In the original model, the grass and weeds were put in the cells as patches while in this implementation as agents. The grass and weeds are handled by a grass agent whose number is the same as the number of cells. The grass agents have two states, grown and grazed. Important to note that grass has a higher chance to grow than weeds. This is because firstly it is decided if weeds can grow and then if grass can grow but it overrides the weeds if it happens. So, if grass can grow due to the set probability then grass will grow disregarding if weeds can grow. This behavior comes from the original model.<br>

As an extension to the model, a predator species can be added which is represented by foxes. The foxes behave basically the same as the rabbits but naturally they eat rabbits. Furthermore, they can also hunt actively which means they only choose such neighboring cells which contain rabbits.<br>

The parameters in order and their default values:<br>

<ul>
<li>The grid's width and height, which can only be changed in the code due to the limitations of the visualization application.
<br><i>30 x 30</i></li>
<li>Torus: If the animal agents are at on of the edges then if they can get to the opposite edge.
<br><i>True</i></li>
<li>Model type, which can either be the original model, the "Rabbits, Grass and Weeds model", or the "Extended model", in which the animals have genders.
<br><i>Rabbits, Grass and Weeds model</i></li>
<li>The initial number of rabbits.
<br><i>150</i></li>
<li>The initial number of foxes.
<br><i>0</i></li>
<li>The rabbits' EP gain from grass and weeds.
<br><i>5 and 0</i></li>
<li>The foxes' EP gain from rabbits.
<br><i>5</i></li>
<li>The rabbits and foxes' maximal initial EP, originally this couldn't be changed.
<br><i>10 and 10</i></li>
<li>The rabbits and foxes' reproduction threshold. An entity needs at least this much EP to reproduce.
<br><i>15 and 15</i></li>
<li>The grass and weeds' regrowth rate in percents. In the original model in thousandths, but the sliders are imprecise in such densely divided interval.
<br><i>6%, originally 15 thousandths or 1,5%</i></li>
<li>If the rabbits can flock.
<br><i>False</i></li>
<li>If the foxes can hunt actively.
<br><i>True</i></li>
<li>The hunt limiter exponent. See below.
<br><i><math xmlns="http://www.w3.org/1998/Math/MathML"><mo>-</mo><mn>0,5</mn></math></i></li>
<li>The random seed. With the help of the seed the runs can be replicated, but it's toggleable.
<br><i>True and 474</i></li>
</ul>

The hunt limiter exponent means that the probability of a fox hunts actively, in other words they only move into those neighboring cell which has rabbits, is
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <msup>
    <mtext>(energy point)</mtext>
    <mrow data-mjx-texclass="ORD">
      <mo>−</mo>
      <mo data-mjx-texclass="ORD" stretchy="false">|</mo>
      <mtext>exponent</mtext>
      <mo data-mjx-texclass="ORD" stretchy="false">|</mo>
    </mrow>
  </msup>
</math>.
So, if the exponent is 0 there's no limitation. It's imortant to note the reason behind the exponent not being positive is that the probability would be 100% just like in case of 0 due to how the code works. Overhunt is typical in case of free hunt this was the motivation behind the exponent.<br>

<br><h3>Extended model</h3>

<ul>
<li>The model type extended by me.</li>
<li>The animal agents have gender.</li>
<li>For reproduction, in addition to the necessary EP two entities with different genders must be present in the same cell.</li>
</ul>

<h2>The visualization application</h2>

<br><h3>Handling</h3>

<img src="rabbitgrassweed/pics/viz_showcase_eng.png" width=700><br>

The figure above is a screenshot of the app in initial state with deafult parameters.<br>

The default language of the webpage is English but by clicking on the flag in the top right corner it can be changed to Hungarian and back. The model's name can be seen in the top left corner, next to it by clicking on the About button README.md's shortened and current language version can be read. The Start, Step and Reset buttons are left to the flag which do what's on the tin but the Start button becomes the Stop button if the simulation is running.<br>

The model's parameters can be set on the left side, the grid that visualizes the model is in the middle, above it the simulation's speed can be set whose default value is 3 steps/second, however the number of agents can effect it (for example in case of overgrowth it's slower). Under the grid the graphs can be seen, among them the 1st one is the number of entities by species and gender depending on the number of steps. The bottom graph is the percentage of the grown grass agents also depending on the number of steps.<br>

The female rabbits are white, the male ones are brown, the female foxes are orange, the male ones are gray. The consequence of this choice is that in the inherited models all rabbits are female and all foxes are male.<br>

<br><h1>References</h1>

<ul>
<li>Wilensky, U. (2001). NetLogo Rabbits Grass Weeds model. <a href=http://ccl.northwestern.edu/netlogo/models/RabbitsGrassWeeds>http://ccl.northwestern.edu/netlogo/models/RabbitsGrassWeeds</a>. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</li>
<li>Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. <a href=http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation>http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation</a>. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</li>
<li><a href=https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg>https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg</a></li>
<li><a href=https://upload.wikimedia.org/wikipedia/commons/a/a5/Flag_of_the_United_Kingdom_(1-2).svg>https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg</a></li>
<li><a href=https://mesa.readthedocs.io/stable/tutorials/visualization_tutorial.html>https://mesa.readthedocs.io/stable/tutorials/visualization_tutorial.html</a> (dead link)</li>
<li><a href=https://stackoverflow.com/questions/66624802/javascript-start-function-when-innertext-changes>https://stackoverflow.com/questions/66624802/javascript-start-function-when-innertext-changes</a></li>
</ul>
