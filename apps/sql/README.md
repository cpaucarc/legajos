## Trigger para correlativo de certificados emitidos:
## Paso 1:
- Crear la secuencia
```
CREATE SEQUENCE public.correlativo_cert_secuencia
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;
```
## Paso 2:
```
CREATE OR REPLACE FUNCTION public.genera_correlativo_cert()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.correlativo := (SELECT LPAD(nextval('correlativo_cert_secuencia') :: TEXT, 5, '0') || '-' || date_part('year', now()));
  RETURN NEW;
END;$function$;
```
## Paso 4:
-  Ejecutar el trigger `trg_correlativo_cert` en la tabla `capacitacion_certemitido`.
```
CREATE TRIGGER trg_correlativo_cert
    BEFORE INSERT
    ON public.capacitacion_certemitido
    FOR EACH ROW
    EXECUTE PROCEDURE public.genera_correlativo_cert();
```
