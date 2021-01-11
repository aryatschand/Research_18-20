# Research_18-20

Implementation of Novel Semi-Supervised Machine Learning Model into Autonomous Irrigation Network Optimized for Power Self-Sufficiency
Written By Arya Tschand 2018-2020

Presentation Video - https://youtu.be/rbFbLL9Grxo

US Provisional Patent Application Number 62799365
US Utility Patent Application Number 16730499

Written in Arduino(C++), VB.net, MySQL, Swift, Python

## Inspiration
While visiting my grandparents in Delhi, I gazed in utter disbelief across endless fields of wilted crops. From conversations with local farmers, I learned that water scarcity was at the root of these crop failures. My growing curiosity led me to investigate how extensive this crisis was worldwide. Like an idle engine waiting for ignition, I found the spark that pushed me to the extent of my creativity and resilience, leading me to pursue water usage inefficiency as the heart of my research project.

## Impact
The constructed autonomous irrigation system is specifically designed to integrate directly into existing infrastructure in developing nations. This ensures that there will not be an income gap that only allows first world farmers to utilize the technology, instead specifically targeting the areas of the world that need the agriculture innovation the most. After extensive practical and theoretical testing of the system, results showed that crop growth efficiency is boosted by nearly 70% with the intelligent methods used and the machine learning model approaches 0% error by the second growth cycle. The project has the potential to make significant impacts in the global water crisis, as well as limit its effect on malnutrition and water scarcity in the most vulnerable regions of the world.

## Technology
In this project, a three-component internet-of-things (IoT)-based irrigation system is designed and constructed to affordably integrate into existing irrigation infrastructure to approach zero water wastage while maintaining crops at a perceived healthy threshold. All components communicate via local area network HTTP communication for high-capacity data transfer with minimal networking infrastructure requirements. A Raspberry Pi-based quadcopter drone and electrical circuit is constructed to collect environmental data and extract brightness-adjusted HSV crop color using k-means clustering-based computer vision algorithms.

An unsupervised recurrent neural network (RNN) component of the irrigation system allows the model to identify correlations between data points and resulting crop health without requiring extensive datasets to provide predictions for optimal irrigation volumes. A many-to-one approach was utilized in the model with a sequence of data points inputted for a single integer output. Long Short Term memory (LSTM) units were found to have better accuracy, and its bidirectional analysis of past and present iterations allows better context analysis of the data and more accurate irrigation volume predictions.

The resulting predicted irrigation volume is executed by an Arduino Nano-based irrigation micropiece to dynamically adjust water flow to each crop for individualized irrigation. Induction from water flow through irrigation pipes generates current, reflecting complete and scalable power self-sufficiency at an excess margin of 25.8%.
