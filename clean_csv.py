input_path = r"c:\Users\Thiago-PC\Desktop\faculdade\cienciasDeDados\Atividade 23-02-2026\Planos De Ação Nacional Para A Conservação Das Espécies Ameaçadas De Extinção (PAN) - 2025 CSV.csv"
output_path = r"c:\Users\Thiago-PC\Desktop\faculdade\cienciasDeDados\Atividade 23-02-2026\Planos De Ação Nacional Para A Conservação Das Espécies Ameaçadas De Extinção (PAN) - 2025 CSV_CLEANED.csv"


def clean_csv(input_p, output_p):
    print(f"Lendo: {input_p}")
    removed_count = 0

    try:
        with open(input_p, "r", encoding="latin-1") as f:
            content = f.read()

        cleaned_chars = []
        for char in content:
            cp = ord(char)
            if (cp >= 32 and cp != 127) or char in "\n\r\t":
                cleaned_chars.append(char)
            else:
                removed_count += 1

        cleaned_content = "".join(cleaned_chars)

        with open(output_p, "w", encoding="utf-8-sig") as f:
            f.write(cleaned_content)

        print("Limpeza concluída!")
        print(f"Caracteres removidos: {removed_count}")
        print(f"Arquivo salvo em: {output_p}")
        return True
    except Exception as e:
        print(f"Erro durante a limpeza: {e}")
        return False


if __name__ == "__main__":
    clean_csv(input_path, output_path)
