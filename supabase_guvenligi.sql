-- ================================================================
-- 1. Öğrenci doğrulama fonksiyonu (sunucu taraflı, güvenli)
--    Türkçe karakter normalizasyonu dahil.
--    SECURITY DEFINER: RLS varken bile çalışır.
-- ================================================================
CREATE OR REPLACE FUNCTION ogrenci_dogrula(
  p_no    INTEGER,
  p_ad    TEXT,
  p_soyad TEXT,
  p_snf   TEXT
)
RETURNS TABLE(no INTEGER, ad TEXT, soyad TEXT, snf TEXT, sube TEXT)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  RETURN QUERY
  SELECT
    s.no,
    s.ad,
    s.soyad,
    s.snf,
    COALESCE(s.sube, '')::TEXT
  FROM students s
  WHERE
    s.no = p_no
    AND upper(translate(trim(s.ad),    'İĞÜŞÖÇığüşöç', 'IGUSOCigusoc'))
      = upper(translate(trim(p_ad),    'İĞÜŞÖÇığüşöç', 'IGUSOCigusoc'))
    AND upper(translate(trim(s.soyad), 'İĞÜŞÖÇığüşöç', 'IGUSOCigusoc'))
      = upper(translate(trim(p_soyad), 'İĞÜŞÖÇığüşöç', 'IGUSOCigusoc'))
    AND trim(s.snf) = trim(p_snf)
  LIMIT 1;
END;
$$;

-- ================================================================
-- 2. Giriş yapmamış kullanıcılar bu fonksiyonu çağırabilsin
--    (sadece evet/hayır döner, liste gelmez)
-- ================================================================
GRANT EXECUTE ON FUNCTION ogrenci_dogrula(INTEGER, TEXT, TEXT, TEXT) TO anon;

-- ================================================================
-- 3. Staff tablosuna kilit (RLS)
--    Artık giriş yapmadan öğretmen/idareci bilgisi okunamaz.
-- ================================================================
ALTER TABLE staff ENABLE ROW LEVEL SECURITY;

CREATE POLICY "sadece_giris_yapanlar" ON staff
  FOR ALL
  TO authenticated
  USING (true)
  WITH CHECK (true);
