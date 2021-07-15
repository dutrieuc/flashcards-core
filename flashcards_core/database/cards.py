from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

CardTag = Table('CardTag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class Card(Base, CrudOperations):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    
    # Deck is 12M because it should be easy to copy cards.
    # Cards hold no actual data: it's just an associative table
    deck_id = Column(Integer, ForeignKey('decks.id'))
    deck = relationship("Deck", foreign_keys='Card.deck_id')

    faces = relationship('Face', back_populates='card')
    reviews = relationship('Review', back_populates='card')
    tags = relationship('Tag', secondary='CardTag', backref='Card')

    def __repr__(self):
        return f"<Card (ID: {self.id}, deck ID: {self.deck_id})>"


    def assign_tag(self, db: Session, tag_id: int, card_id: int) -> CardTag:
        """
        Assign the given Tag to this Card.

        :param tag_id: the name of the Tag to assign to the Card.
        :param card_id: the name of the Card to assign the Tag to.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: the new CardTag model object.
        """
        db_cardtag = CardTag(tag_id=tag_id, card_id=card_id)
        db.add(db_cardtag)
        db.commit()
        db.refresh(db_cardtag)
        return db_cardtag


    def remove_tag(self, db: Session, cardtag_id: int) -> None:
        """
        Remove the given Tag from this Card.

        :param cardtag_id: the ID of the connection between a tag and a card.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: None.

        :raises: ValueError if no CardTag object with the given ID was found in the database.
        """
        db_cardtag = db.query(CardTag).filter(CardTag.id == cardtag_id).first()
        if not db_cardtag:
            raise ValueError(f"No CardTag with ID '{cardtag_id}' found. Cannot delete non-existing connection.")
        db.delete(db_cardtag)
        db.commit()

