DROP FUNCTION blog_article_trigger ();
DROP TRIGGER blog_article_tsv_update ON blog_article;


ALTER TABLE blog_article ADD COLUMN tsv tsvector;

CREATE FUNCTION blog_article_trigger() RETURNS trigger AS 
$$
begin
  new.tsv :=
     setweight(to_tsvector('pg_catalog.russian', new.name), 'A') ||
     setweight(to_tsvector('pg_catalog.russian', new.text), 'B');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE TRIGGER blog_article_tsv_update BEFORE INSERT OR UPDATE
ON blog_article FOR EACH ROW EXECUTE PROCEDURE blog_article_trigger();