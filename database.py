import sqlite3

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def _execute_query(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        """Вспомогательный метод для работы с SQL, чтобы не дублировать код"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        
        if commit:
            conn.commit()
            
        conn.close()
        return result

    def init_db(self):
        """Создание таблицы и начальное заполнение"""
        query = '''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT UNIQUE NOT NULL,
                subjects TEXT NOT NULL
            )
        '''
        self._execute_query(query, commit=True)
        
        # Если база пустая — добавим стандартные дни
        if not self.get_all_days():
            initial_data = [
                ("Понедельник", "Математика, Русский язык, Информатика"),
                ("Вторник", "Физика, Английский язык, Геометрия"),
                ("Среда", "Биология, История, Обществознание"),
                ("Четверг", "Химия, Литература, География"),
                ("Пятница", "Алгебра, Физкультура, ОБЖ")
            ]
            for day, subs in initial_data:
                self._execute_query("INSERT INTO schedule (day, subjects) VALUES (?, ?)", (day, subs), commit=True)

    def get_day_schedule(self, day_name):
        res = self._execute_query("SELECT subjects FROM schedule WHERE day = ?", (day_name,), fetchone=True)
        return res[0] if res else "Уроков нет"

    def get_all_days(self):
        res = self._execute_query("SELECT day FROM schedule", fetchall=True)
        return [row[0] for row in res]

    def get_full_schedule(self):
        """Для кнопки 'Все уроки'"""
        return self._execute_query("SELECT day, subjects FROM schedule", fetchall=True)