CREATE TABLE users (
    id char(36) NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    age int NOT NULL,
    biography text NULL,
    city varchar(50) NULL,
    created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    password_hash varchar(255) NOT NULL,
    CONSTRAINT newtable_pk PRIMARY KEY (id)
);


CREATE TABLE public.friends (
    id char(36) NOT NULL,
    user char(36) NOT NULL,
    friend char(36) NOT NULL,
    CONSTRAINT friends_pk PRIMARY KEY (id),
    CONSTRAINT friends_user_FK FOREIGN KEY (user) REFERENCES public.users(id),
    CONSTRAINT friends_friend_FK FOREIGN KEY (friend) REFERENCES public.users(id)
);

CREATE INDEX friends_user_idx ON public.friends (user);
CREATE INDEX friends_friend_idx ON public.friends (friend);


CREATE TABLE posts (
      id char(36) NOT NULL,
      author_user_id char(36) NOT NULL,
      text text NOT NULL,
      created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
      PRIMARY KEY (id),
      CONSTRAINT posts_FK FOREIGN KEY (author_user_id) REFERENCES public.users(id)
    );


CREATE TABLE public.dialogs (
    id bpchar NOT NULL,
    partion_id int8 NOT NULL,
    from_user_id bpchar NOT NULL,
    to_user_id bpchar NOT NULL,
    "text" text NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT dialogs_pk PRIMARY KEY (id),
    CONSTRAINT dialogs_fk_1 FOREIGN KEY (to_user_id) REFERENCES public.users(id),
    CONSTRAINT dialogs_fk_2 FOREIGN KEY (from_user_id) REFERENCES public.users(id)
);
CREATE INDEX dialogs_from_user_id_idx ON public.dialogs USING btree (from_user_id);
CREATE INDEX dialogs_to_user_id_idx ON public.dialogs USING btree (to_user_id);