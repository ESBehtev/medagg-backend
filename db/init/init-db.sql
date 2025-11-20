--
-- Here can be put some initial logic to be ran on db creation.
--

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE anatomical_areas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE modalities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- НОВАЯ ТАБЛИЦА: Типы ML-задач
CREATE TABLE ml_tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    external_link VARCHAR(1000),
    local_storage_path VARCHAR(500),
    record_count INTEGER,
    dataset_size_mb INTEGER,

    -- Связи
    anatomical_area_id INTEGER REFERENCES anatomical_areas(id),

    -- Метаданные
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Датасеты и модальности
CREATE TABLE dataset_modalities (
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    modality_id INTEGER NOT NULL REFERENCES modalities(id),
    PRIMARY KEY (dataset_id, modality_id)
);

-- НОВАЯ: Датасеты и ML-задачи
CREATE TABLE dataset_ml_tasks (
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    ml_task_id INTEGER NOT NULL REFERENCES ml_tasks(id),
    PRIMARY KEY (dataset_id, ml_task_id)
);

-- Теги
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE dataset_tags (
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id),
    PRIMARY KEY (dataset_id, tag_id)
);

CREATE TABLE user_dataset_collections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Метаданные сборки
    storage_path_hdfs VARCHAR(500) NOT NULL, -- Путь к архиву в HDFS
    archive_size_mb INTEGER, -- Размер итогового архива

    -- временные метки
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

CREATE TABLE user_search_queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id), -- Может быть NULL для анонимных поисков
    query_text TEXT NOT NULL,
    filters JSONB, -- Сохраненные фильтры поиска (области, модальности, задачи и т.д.)
    performed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Связь: какие датасеты вошли в сборку пользователя
CREATE TABLE collection_datasets (
    collection_id INTEGER NOT NULL REFERENCES user_dataset_collections(id) ON DELETE CASCADE,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id),
    relevance_score DECIMAL(5,4), -- Оценка релевантности от ИИ-модели (если доступна)
    query_id INTEGER NOT NULL REFERENCES user_search_queries(id) ON DELETE CASCADE,
    PRIMARY KEY (collection_id, dataset_id)
);

CREATE OR REPLACE FUNCTION set_expires_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.expires_at = NEW.created_at + INTERVAL '1 day';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггер
CREATE TRIGGER set_expiration_date
    BEFORE INSERT ON user_dataset_collections
    FOR EACH ROW
    EXECUTE FUNCTION set_expires_at();
