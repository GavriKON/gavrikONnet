# SOCIAL NETWORK by GavrikON

## Info:

*  Just a personal project to build skills in Backend. When you try to clone a project to a local repository, there will be no data in the database.Just a personal project to build skills in Backend. When you try to clone a project to a local repository, there will be no data in the database.

## Installation

##### Dependencies: ***Windows** or Linux, Git, Docker.*

1. `git clone https://github.com/GavriKON/gavrikONnet.git`
2. `cd .\gavrikONnet`
3. Create an `.env` file with the following content:

>
> DATABASE_URL=postgresql://DB_USER:DB_PASSWORD@db:5432/DB_NAME # Path to your DB (Postgres)
>
> SECRET_KEY=dce6f1185c254cx/220f271c97f549ba67 # Using against modifying cookies and cross-site request forgery attacks
>
> EMAIL_USER=gavrilin115@gmail.com #Email from which password recovery emails will be sent
>
> EMAIL_PASS=jmekoqowxspikngt #Use App Passwords in Security Settings (In gmail)
>
> FLASK_APP = run.py #Deafault
>
> POSTGRES_USER=DB_USER
>
> POSTGRES_PASSWORD=DB_PASSWORD
>
> POSTGRES_DB=DB_NAME
>
> PGADMIN_DEFAULT_EMAIL=PG_ADMIN_EMAIL # Example: root@gmail.com
>
> PGADMIN_DEFAULT_PASSWORD=PG_ADMIN_PASSWORD # Password for pgadmin in browser
>
> PGADMIN_LISTEN_ADDRESS=0.0.0.0 # so that there are no problems with nginx, it is better to be on the same network with the app
>
> PGADMIN_LISTEN_PORT=5555

4. `docker-compose -f docker-compose.yaml up -d --build`
5. `docker exec flask_azz_yt flask commands create_db` # Initialize, **create a new table into the database.**
6. Open `http://localhost/home` in browser.
