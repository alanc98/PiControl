//  Hello World client
#include <zmq.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>

void *context;
void *requester;

int main (void)
{
    printf ("Connecting to BMP Sensor Server\n");
    context = zmq_ctx_new ();
    requester = zmq_socket (context, ZMQ_REQ);
    zmq_connect (requester, "tcp://localhost:5555");

    while(1)
    {
        char buffer [80];
        printf ("Sending Request\n");
        zmq_send (requester, "SENSOR_REQ,DEV=ADA_BMP180,SUB_DEV=BMP,CMD=READ,SENSOR_REQ_END", 41, 0);
        zmq_recv (requester, buffer, 80, 0);
        printf ("Received: %s\n", buffer);
    }
    zmq_close (requester);
    zmq_ctx_destroy (context);
    return 0;
}
