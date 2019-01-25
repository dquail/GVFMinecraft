# Abstract
This project looks to accomplish two goals. First, it lays out a framework for using a layered network of predictions, based on raw sensorimotor data, to represent knowledge. These “predictions” are represented 

using general value functions - a function common in reinforcement learning, which allows the agent to ask a question about its raw sensorimotor data, and then based on experience, begin to learn estimates for these questions. Secondly, we look to conduct experiments using Minecraft whereby an agent can sense a wall, and move forward or turn, to begin to ask questions
about its environment using the simple sensorimotor data. The questions respective answers begin to be- come more and more abstract and sophisticated as the GVSs are layered on top of each other. In a sense, this will offer insights into how the agent can not only represent, but learn these representations. This implementation demonstrates how an artificial intelligence agent can build useful abstract knowledge from its raw sensorimotor experience alone using a network of General Value functions. This paper shares the design of such a learning agent and preliminary results.GVFs are rooted in the most primitive sensorimotor observations from the environment, and can be layered to form increasingly more abstract knowledge. Such a view of learning is often referred to as constructivist. In this constructivist life long learning agent architecture, that the GVF is the single mechanism to bridge the gap from low level sensorimotor interaction to abstract knowledge.

A very early draft of the research paper can be found [here](RepresentingHighLevelKnowledge.pdf)