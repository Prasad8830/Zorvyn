from app.db.database import SessionLocal
from app.db.models import User, RoleEnum
from app.core.security import get_password_hash

def seed_super_admin():
    db = SessionLocal()
    admin_email = "admin@zorvyn.com"
    admin_password = "adminpassword123"
    
    # Check if admin already exists
    user = db.query(User).filter(User.email == admin_email).first()
    if user:
        print(f"Admin user already exists. Email: {admin_email}")
        db.close()
        return
        
    # Create the admin user
    hashed_pw = get_password_hash(admin_password)
    new_user = User(
        email=admin_email,
        hashed_password=hashed_pw,
        role=RoleEnum.admin,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    print(f"✅ Fast-bootstrapped Admin Account!")
    print(f"📧 Username: {admin_email}")
    print(f"🔑 Password: {admin_password}")
    db.close()

if __name__ == "__main__":
    seed_super_admin()