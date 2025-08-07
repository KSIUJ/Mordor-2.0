-- If you want to write database tables manually you can do it here.
-- Files in this directory are executed in lexecographical order by the database engine.
-- It is defined in docker-compose.yml file.

-- When you modify those files to make changes visible you need to stop the docker container of database
-- rm -rf .pgdata folder which is mounted to the container and start container again.
-- This is very uncomfortable in bigger projects if database scheme is not predefined migration tools are used.

-- .pgdata is mounted folder and it is persistent till you remove it. So u can easily use it 
-- and modify database using psql or any other tool. But remember to later export it to .sql file and put it here.
-- so you can use it in the future.