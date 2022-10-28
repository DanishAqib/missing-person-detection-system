import uuid

users_table = """
    create table if not exists users
    (
        u_id uuid not null primary key,
        u_name varchar(50) not null,
        u_password varchar(50) not null,
        u_created_at timestamp default current_timestamp
    )"""

submitted_cases_table = """
    create table if not exists submitted_cases
    (
        sc_id uuid not null primary key,
        sc_submitted_by uuid references users(u_id) not null,
        sc_name varchar(50) not null,
        sc_age int not null,
        sc_gender varchar(10) not null,
        sc_last_seen_location varchar(50) not null,
        sc_case_status varchar(50) not null,
        sc_case_image text not null,
        sc_face_encoding jsonb not null,
        sc_created_at timestamp default current_timestamp,
        sc_submitted_at timestamp default current_timestamp
    )"""

detected_persons_table = """
    create table if not exists detected_persons
    (
        dp_id uuid not null primary key,
        dp_case_id uuid references submitted_cases(sc_id),
        dp_location varchar(50) not null,
        dp_detected_image text not null,
        dp_detected_at timestamp default current_timestamp
    )"""
    
default_user_query = "insert into users (u_id, u_name, u_password) values ('{}', '{}', '{}')".format(
    str(uuid.uuid4()), "admin", "admin")