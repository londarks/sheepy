```
JWR Refresh Token
                         +----------------+       
                         |                |       
                         |    Client App   |       
                         |                |       
                         +-------+--------+       
                                 |                 
                                 | Request Access 
                                 |                 
                         +-------v--------+       
                         |                |       
                         |  Authentication|       
                         |     Server     |       
                         |                |       
                         +-------+--------+       
                                 |                 
                         +-------v--------+       
                         |                |       
                         |    Authorization|      
                         |     Server     |       
                         |                |       
                         +-------+--------+       
                                 |                 
                                 | Issue JWT       
                                 |                 
                         +-------v--------+       
                         |                |       
                         |   Client App    |       
                         |                |       
                         +-------+--------+       
                                 |                 
                                 | Access Resources 
                                 |                 
                         +-------v--------+       
                         |                |       
                         |  Protected API  |       
                         |                |       
                         +----------------+    

```