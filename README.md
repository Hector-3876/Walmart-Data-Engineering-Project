# Walmart-Data-Engineering-Project

Explicando la arquitectura, 
- tenemos de ingesta (S3 aws) y una Agentic DB (hosteada gratis en GHOST) https://ghost.build/
- Cargaremos estos datos de entrada a nuestra bronze layer en databricks. Al usar CDC en nuestra DB estaremos únicamente cargando datos nuevos posterior a la última carga.
- Para transformaciones usaremos DBT, hasta llegar a nuetra ONE-BIG-TABLE
- En esta OBT haremos quality checks.
- Una vez que nuestra OBT (silver layer) esté lista, pasaremos a nuestra golden layer.
- Nuestra (golden layer) será un star schema con SCD 2 (nota: el star schema obviamente estará desnormalizado para facilitar el análisis)

todo este proceso lo orquestaremos con Airlfow.


Ventajas de usar CDC, principalmente UPSERT, si hay nuevos datos los inserta, si le cambia algo a los datos existentes los actualiza, ya no necesitamos idempotencia
