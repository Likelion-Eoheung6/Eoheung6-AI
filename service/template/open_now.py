from datetime import datetime

# FIXME
class TemplateSql(FilterOpenClass):
    def filter(self, class_id, db_session):
        now = datetime.now()
        query = """
            SELECT co.class_id, c.class_name, c.description
            FROM class_open co
            JOIN class c ON co.class_id = c.id
            WHERE co.is_closed = FALSE
            AND co.open_at <= NOW()
            AND co.class_id IN (%s)  -- Qdrant에서 가져온 ID 목록
        """
        db_session.execute(query, (tuple(class_id),))
        return db_session.fetchall()