from constants import *
missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                  <DrawingDecorator>
                    <DrawLine x1="20" y1="56" z1="-20" x2="20" y2="56" z2="100" type = "sand"/>
              
                    <DrawLine x1="11" y1="56" z1="-20" x2="-50" y2="56" z2="-20" type = "gold_block"/>
              
                    <DrawLine x1="-20" y1="56" z1="-8" x2="-20" y2="56" z2="20" type = "brick_block"/>
              
                    <DrawLine x1="-10" y1="56" z1="20" x2="9" y2="56" z2="20" type = "diamond_block"/>
              
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="56" z="0.5" yaw="0"/>
                </AgentStart>
                <AgentHandlers>
                    <VideoProducer want_depth="false">
                        <Width>''' + str(WIDTH) + '''</Width>
                        <Height>''' + str(HEIGHT) + '''</Height>
                    </VideoProducer>
                    <ObservationFromGrid>
                        <Grid name="floor3x3">
                            <min x="-1" y="0" z="-1"/>
                            <max x="1" y="0" z="1"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromFullStats/>
                    <DiscreteMovementCommands />
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


mission3HeightXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                  <DrawingDecorator>
                    <DrawLine x1="20" y1="56" z1="-20" x2="20" y2="56" z2="100" type = "sand"/>
                    <DrawLine x1="20" y1="57" z1="-20" x2="20" y2="57" z2="100" type = "sand"/>
                    <DrawLine x1="20" y1="58" z1="-20" x2="20" y2="58" z2="100" type = "sand"/>
                    <DrawLine x1="20" y1="59" z1="-20" x2="20" y2="59" z2="100" type = "sand"/>

                    <DrawLine x1="11" y1="56" z1="-20" x2="-50" y2="56" z2="-20" type = "gold_block"/>
                    <DrawLine x1="11" y1="57" z1="-20" x2="-50" y2="57" z2="-20" type = "gold_block"/>
                    <DrawLine x1="11" y1="58" z1="-20" x2="-50" y2="58" z2="-20" type = "gold_block"/>
                    <DrawLine x1="11" y1="59" z1="-20" x2="-50" y2="59" z2="-20" type = "gold_block"/>

                    <DrawLine x1="-20" y1="56" z1="-8" x2="-20" y2="56" z2="20" type = "brick_block"/>
                    <DrawLine x1="-20" y1="57" z1="-8" x2="-20" y2="57" z2="20" type = "brick_block"/>
                    <DrawLine x1="-20" y1="58" z1="-8" x2="-20" y2="58" z2="20" type = "brick_block"/>
                    <DrawLine x1="-20" y1="59" z1="-8" x2="-20" y2="59" z2="20" type = "brick_block"/>                    

                    <DrawLine x1="-10" y1="56" z1="20" x2="9" y2="56" z2="20" type = "diamond_block"/>
                    <DrawLine x1="-10" y1="57" z1="20" x2="9" y2="57" z2="20" type = "diamond_block"/>
                    <DrawLine x1="-10" y1="58" z1="20" x2="9" y2="58" z2="20" type = "diamond_block"/>
                    <DrawLine x1="-10" y1="59" z1="20" x2="9" y2="59" z2="20" type = "diamond_block"/>    

                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="56" z="0.5" yaw="0"/>
                </AgentStart>
                <AgentHandlers>
                    <VideoProducer want_depth="false">
                        <Width>''' + str(WIDTH) + '''</Width>
                        <Height>''' + str(HEIGHT) + '''</Height>
                    </VideoProducer>
                    <ObservationFromGrid>
                        <Grid name="floor3x3">
                            <min x="-1" y="0" z="-1"/>
                            <max x="1" y="0" z="1"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromFullStats/>
                    <DiscreteMovementCommands />
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
