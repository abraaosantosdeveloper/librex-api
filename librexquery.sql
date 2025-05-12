create database librex;
use librex;

create table users(
	id int auto_increment not null,
    fname varchar(60) not null,
    sname varchar(60) not null,
    bdate date not null,
    displayname varchar(60) not null,
    admin tinyint default 0,
    banned tinyint default 0,
    email varchar(120) not null,
    password varchar(255) not null,
    created_at datetime default current_timestamp,
    primary key(id)
);

create table authors(
	id int auto_increment not null,
    name varchar(200),
    primary key(id)
);

create table genres(
	id int auto_increment not null,
    genre varchar(100),
    created_at datetime default current_timestamp,
    primary key(id)
);


create table books(
	id int auto_increment not null,
    title varchar(120) not null,
    synopsis varchar(2000),
	author_id int,
    genre_id int,
    pages int not null,
    public tinyint default 0,
    created_at datetime default current_timestamp,
    user_id int,
    
    primary key(id),
    constraint fk_author_id foreign key(author_id) references authors(id) on delete set null,
    constraint fk_user_id foreign key(user_id) references users(id) on delete set null,
	constraint fk_genre_id foreign key(genre_id) references genres(id) on delete set null
);

CREATE TABLE evaluations(
    id INT AUTO_INCREMENT NOT NULL,
    grade INT NOT NULL,
    user_id INT,
    book_id INT,
    created_at datetime default current_timestamp,
    PRIMARY KEY(id),
    CONSTRAINT fk_user_id_evaluations FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_book_id_evaluations FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
);

create table comments(
	id int auto_increment not null,
    evaluation_id int,
    comment varchar(500),
    created_at datetime default current_timestamp,
    primary key(id),
    constraint fk_evaluation_id foreign key(evaluation_id) references evaluations(id) on delete cascade
);

create table messages(
	id int auto_increment not null,
    sender_id int,
    recipient_id int,
    title varchar(100) not null,
    content varchar(2000) not null,
    created_at datetime default current_timestamp,
    
    primary key(id),
    constraint fk_sender_id foreign key(sender_id) references users(id) on delete cascade,
    constraint fk_recipient_id foreign key(recipient_id) references users(id) on delete cascade
);

create table banned_users(
	id int auto_increment not null,
    user_id int,
    reason varchar(300),
    banned_at date,
	primary key(id),
    constraint fk_user_id_banned_users foreign key(user_id) references users(id) on delete cascade
);

create table favorites(
    user_id int,
    book_id int,
    created_at datetime default current_timestamp,
    primary key(user_id, book_id),
    constraint fk_user_id_favorites foreign key(user_id) references users(id) on delete cascade,
    constraint fk_book_id_favorites foreign key(book_id) references books(id) on delete cascade
);

-- Trigger de publicação de livro

DELIMITER $$

CREATE TRIGGER after_book_published
AFTER UPDATE ON books
FOR EACH ROW
BEGIN

    IF NEW.public = 1 AND (OLD.public IS NULL OR OLD.public = 0) THEN
        INSERT INTO messages (sender_id, recipient_id, title, content)
        VALUES (
            1,
            NEW.user_id,
            'Publicação Aprovada!',
            CONCAT('Seu livro "', NEW.title, '" foi aprovado pela nossa equipe. Agora ele está visível para todos os leitores. Parabéns!')
        );
    END IF;
END $$

DELIMITER ;
