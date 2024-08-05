# gestionDeportes

Realizado por: Emilio Jaramillo.

Es un sistema que permite manejar un campeonato deportivo, para algunos deportes, especialmente para futbol, hecho con el framework de django, y utilizando programacion orientada a objetos, cumpel con los requerimentos de:

- Inscribir un equipo a diferentes campeonatos con diferentes deportistas
- Manejar el resultado 2 a 2 de un partido
- Manejar la tabla de Posiciones de los campeonatos

-Diagrama de Clases:

![diagramaUML](https://github.com/user-attachments/assets/91b350af-79ff-44fc-bc75-4aa48aac8214)

-Como ejecutar el proyecto

Para ejecutar el proyecto se debe seguir los siguientes pasos:

1. Clonar el repositorio en una nueva carpeta o descargar como archivo zip y descomprimir en la carpeta.

![image](https://github.com/user-attachments/assets/abc8519f-ecca-483a-b4d4-422afbfe80b9)

2. Acceder a la consola e ingresar los siguientes comandos:

   2.1. Instalar virtualenv y asignar al proyecto:

   pip install virtualenv
   
   virtualenv venv

   ![image](https://github.com/user-attachments/assets/fd0ebad0-e3c2-411a-be95-ed9ede5e8af9)

   2.2. Activar el virtualenv

   ![image](https://github.com/user-attachments/assets/0614a230-bc3c-4014-9d40-73cdb51be9c1)

   2.3. Instalar Django

   pip install django

   ![image](https://github.com/user-attachments/assets/cc94f525-c22b-4a56-a394-c1c14955bd8f)

   2.4. Inicializar el servidor:
   
   Primeros nos dirijimos a la ubicacion del manage.py

   cd gestionDeportes/gestion_campeonato

   python manage.py runserver

   ![image](https://github.com/user-attachments/assets/9cd1cfae-0e48-48d1-8834-732871d79016)

   2.5. Listo, finalmente solo se debe acceder al puerto local desde cualquier navegador:
   
   ![image](https://github.com/user-attachments/assets/c6e96bd9-41fa-402e-b571-32633719c56c)


-Funcionamiento:

 -Crear Campeonato
 
 ![image](https://github.com/user-attachments/assets/bb979b85-e83f-435c-b837-e3f997c78663)
 
 Aqui podremos crear un nuevo campeonato rellenando los espacios del formulario con la informacion necesaria
 
 -Crear Equipo
 
 ![image](https://github.com/user-attachments/assets/3381d50d-3ac7-4696-a222-8a1223bf5e3e)
 
 De igual manera podemos crear un nuevo equipo con el formulario.
 
 -Inscribir Equipo
 
 ![image](https://github.com/user-attachments/assets/09726d98-fca0-49ef-8899-110a84e44578)
 
 Con este formulario vamos a poder inscribir un equipo a un campeonato, el equipo solo se puede inscribir una sola vez al campeonato, y todos los equipos se pueden inscribir a diferentes campeonatos.
 
 -Lista de Campeonatos
 
 ![image](https://github.com/user-attachments/assets/d187c11d-6b57-4156-9325-9a29dae48dee)
 
 Aqui nos apareceran todos los campeonatos generados y un acceso al detalle de cada campeonato
 
 -Detalle de Campeonato
 
 ![image](https://github.com/user-attachments/assets/14cc6237-2140-4717-9d10-0f54a51b5f70)
 
 Aqui nos aparece el detalle del campeonato, con los equipos inscritos, un boton para inicializar el campeonato, los partidos creados para ese campeonato, un formulario para crear partidos, y la tabla de posiciones del campeonato
 
 En el detalle de cada Equipo, tenemos dos accesos uno para ver el detalle del equipo, y otro para eliminar ese equipo de ese campeonato, 
 
 ![image](https://github.com/user-attachments/assets/7cecd367-8ac1-4a0e-a237-de6566bda253)
 
 -Detalle de Equipo
 
 ![image](https://github.com/user-attachments/assets/65b2db66-f3f0-4603-ae44-5cf62599f4a1)
 
 En esta vista tenemos el detalle del equipos, asi como la lista de deportistas que estan en el equipo en esa participacion a ese campeonato, ademas tenemos un acceso para ver el detalle de cada deportista, y otra para eliminar a ese deportisra, ademas al final tenemos un acceso para agregar un nuevo deportista a la participacion del equipo.
 
 -Agregar Deportista
 
 ![image](https://github.com/user-attachments/assets/81d56d2b-103e-4db3-b0ad-78b7ade14bf8)
 
 Aqui mediante el formulario se puede agregar un nuevo deportista al equipo
 
 -Detalle del Deportista
 
 ![image](https://github.com/user-attachments/assets/590a10bd-dc36-422f-b3ee-ebb7d1cecd28)
 
 Aqui podemos ver el detalle del deportista.
 
 
