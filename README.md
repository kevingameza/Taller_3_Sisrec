# Taller_2_Sisrec

Run docker file
```
docker-compose up --build
```

Stop docker
```
docker-compose down
```

fill db
```
docker-compose exec db psql -U postgres -d postgres -f /var/lib/postgresql/csv-data/init.sql
```
