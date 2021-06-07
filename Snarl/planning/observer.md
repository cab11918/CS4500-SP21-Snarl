
    
**TO:** Manager      
**FROM:** Minghao Yu, Yuan Wang      
**DATE:** 03/11/2021      
**SUBJECT:** Gane Observer specification  
      
## Game Observer  
  
The Game Observer is an interface that was used for debugging and also presenting the game to the stakeholders with a visual representation. The stakeholders can see the information rendered but they don't have the permission to control any characters.  
  
The Game Observer will listen for any operations happened in Game Manager and render them accordingly. The data representation we use for the communication between those two components is JSON. Any updates and changes in Game Manager with the state will be notified by calling ``update`` function which were mentioned below.  
    
The Game Observer should consist of the following variables:    
* ``parsed_state`` - A state representation that was parsed from the JSON representation of the Game Manager.  
* ``logs`` - A list of log messages that came from the Game Manager. The messages will eventually be printed to the viewer of the game.  
  
---    
 ## Game Observer Interface  
  ``update_log(msg)`` -  this function will be called by the main program (a main program is something we assume to be a connecting component between Gama Manager and Game Observer) and store the message to the log list for debugging/presenting purpose.  
 * params: msg - a JSON value which represent the operation happened that was sent by Game Manager    
 * return: None    
 * throw: Exception - any error during the parsing process    
  
 ``update_state(state)`` - this function will be called by the main program and it stores the updated state parsed from the JSON value it received.  
 * params: state - a JSON value to represent state that was sent by Game Manager    
 * return: None    
 * throw: Exception - any error during the parsing process    
  
``render_state()`` - this function will use the ``state`` that was received from the Game Manager and render it with GUI library to generate a visual representation.  
 * params: None  
 * return: None    
 * throw: Exception - any error during the GUI construction   
  
---  
Note: Based on the fact that it's still possible that in future implementation, there will be no intermediate component, we would consider making our update function take in state model directly.