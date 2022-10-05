# A-Star-Search-Graph-Visualization
Program to create a mock map with city nodes and road connections
The program will then be able to, given a start city and end city, show user the shortest path to their destination
This is meant to be a very simplified vision of Google Maps!
-----------------------------------
Controls:
Mouse inputs:
"LEFT_CLICK"  = If clicked and held over a city nodes, will allow user to move city node
"RIGHT_CLICK" = If clicked on a city node will allow user to link city nodes together.
                First click is to set the parent city node, then following clicks set the destination 
                city nodes. Click "l" to lock all destination city nodes to starting city

Keyboard inputs:
"c"      = Create city node at given mouse(x,y).
"l"      = Will create links between respective selected city nodes.
"r"      = Will remove links between respective selected city nodes.
"DELETE" = Resets the map.
"ESCAPE" = Will exit the program.

Preview of current program:
![2022-10-05 (1)](https://user-images.githubusercontent.com/62959991/193979555-83928077-aeb5-40b7-9c3d-14d4006c3c28.png)
![2022-10-05](https://user-images.githubusercontent.com/62959991/193979551-68406918-dc18-424b-8d71-4e2fbbf0f98b.png)