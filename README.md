# A-Star-Search-Graph-Visualization
Program to create a mock map with city nodes and road connections.
The program will then be able to, given a start city and end city, show user the shortest path to their destination.
This is meant to be a very simplified version of Google Maps!
-----------------------------------
Controls:
Mouse inputs:
- "LEFT_CLICK"  = If clicked and held over a city nodes, will allow user to move city node
- "RIGHT_CLICK" = If clicked on a city node will allow user to link city nodes together.
                First click is to set the parent city node, then following clicks set the destination 
                city nodes. Click "l" to lock all destination city nodes to starting city

Keyboard inputs:
- "c"      = Create city node at given mouse(x,y).
- "l"      = Will create links between selected city nodes.
- "r"      = Will remove links between selected city nodes.
- "m"      = Will set start and destination city nodes
- "s"      = Following setup with "m", this will find the shortest path, and mark it in red. With any movement of the city nodes,
             the shortest path will update if a new path is found
- "DELETE" = Resets the map.
- "ESCAPE" = Will exit the program.

Previews:

Map showing the shortest path between start and destination cities!
![Screenshot_108](https://user-images.githubusercontent.com/62959991/194614572-0a202929-17aa-49e2-a628-4ba8f2efef16.png)
![2022-10-06 (6)](https://user-images.githubusercontent.com/62959991/194217646-e652eeda-b37d-47de-85f4-958f9d320e3e.png)
Map after some city node movements, notice path has updated!
![2022-10-06 (7)](https://user-images.githubusercontent.com/62959991/194217686-d4a4b919-a3e6-452c-8e19-28a0f087741a.png)
Map after setting up connections and nodes
![2022-10-05 (1)](https://user-images.githubusercontent.com/62959991/193979555-83928077-aeb5-40b7-9c3d-14d4006c3c28.png)
Map after selecting start and destination
![2022-10-06 (5)](https://user-images.githubusercontent.com/62959991/194217827-b81d5f9f-28da-4aa0-89a4-e70b4d8711b5.png)
