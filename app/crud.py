from sqlalchemy.orm import Session
import models, schemas
from models import Telegram, Products

def get_items(model, db: Session, limit: int= 10):

    if model == Telegram:
        telegrams = db.query(Telegram).limit(limit).all()

        for telegram in telegrams:
            telegram.Date = str(telegram.Date)

        return telegrams

    return db.query(model).limit(limit).all()


def get_item_by_id(model, db: Session, item_id):
    
    if model == Telegram:
        telegram = db.query(model).filter(model.ID == item_id).first()
        telegram.Date = str(telegram.Date)

        return telegram
    
    return db.query(model).filter(model.ID == item_id).first()


def create_item(model, db: Session, item):
    db_item = model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(model, db: Session, item_id):
    db_item = db.query(model).filter(model.ID == item_id).first()
    if db_item is None:
        return None     
    db.delete(db_item)
    db.commit()
    return db_item


def update_item(model, db: Session, item_id, update_data: dict):
    db_item = db.query(model).filter(model.ID == item_id).first()
    if db_item:
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)    
        return db_item
    return None