createdb caravel

create role caravel;

alter role caravel with login;
alter role caravel with password 'mahdimazaheri';

#########

CREATE EXTENSION postgres_fdw WITH SCHEMA foreign_data ;


CREATE SERVER miare_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (
    dbname 'miare',
    host 'www.miare.ir',
    port '5432'
);


CREATE USER MAPPING FOR caravel SERVER miare_server OPTIONS (  
    password 'itmaysnow',
    "user" 'caravel'
);

\connect caravel

CREATE SCHEMA foreign_data;

ALTER USER caravel WITH superuser ;

## login with caravel

CREATE EXTENSION postgis WITH SCHEMA public ;

IMPORT FOREIGN SCHEMA public FROM SERVER miare_server INTO foreign_data;

