import bcrypt

class PasswordManager:
    DEFAULT_SALT_ROUNDS = 12

    @staticmethod
    def hash_password(password: str, rounds: int = DEFAULT_SALT_ROUNDS) -> bytes:
        # Verificar se a senha fornecida atende aos requisitos de tamanho e complexidade
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Gerar um salt aleatório com custo especificado
        salt = bcrypt.gensalt(rounds=rounds)
        
        # Criptografar a senha usando o salt gerado
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        # Verificar se o valor do hash armazenado começa com o prefixo "$2b$"
        if not hashed_password.startswith(b"$2b$"):
            raise ValueError("Invalid hash value")
        
        # Verificar se a senha fornecida corresponde ao hash armazenado
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        except (ValueError, TypeError):
            return False
