credentials for program:

USERNAME: admin
PASSWORD: adm1n



Please note, when running the file in playground, or in cmd line, the PDF provided commands did not run the file correctly.
The error was that when selecting a menu option, the program would return invalid selection for valid inputs.

when running in cmd.exe, instead of:

docker run -i python-app

use:

docker run -it python-app



When running on a VM in Docker Playground, instead of:

docker run -d -p 80:80 [user]/[repo]

use:

docker run -it -p 80:80 [user]/[repo]



Link to docker repository:

https://hub.docker.com/repository/docker/chatsim/l3t8ct2

Dockerfile contained in folder "Compulsory Task 2"