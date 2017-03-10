#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

int maint(int argc, char *argv[]){
  
  if(argv[1]=='server'){
    //ajustes server
    host=argv[2];//tiene que ser =''???
    port=argv[3];
      
    init_server(host,port)
  }
  if( argv[1]=='client'){
    //ajustes de client
    host=argv[2];
    port=argv[3];
    init_client(host, port)
  }

}
