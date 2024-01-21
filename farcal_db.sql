PGDMP  :                     |         	   farcal_db    16.0    16.0     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16729 	   farcal_db    DATABASE     �   CREATE DATABASE farcal_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE farcal_db;
                postgres    false            �            1259    16804    agriculturalperiods    TABLE     �   CREATE TABLE public.agriculturalperiods (
    periodid integer NOT NULL,
    periodname character varying(255) NOT NULL,
    startdate date NOT NULL,
    enddate date NOT NULL
);
 '   DROP TABLE public.agriculturalperiods;
       public         heap    postgres    false            �            1259    16803     agriculturalperiods_periodid_seq    SEQUENCE     �   CREATE SEQUENCE public.agriculturalperiods_periodid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.agriculturalperiods_periodid_seq;
       public          postgres    false    218            �           0    0     agriculturalperiods_periodid_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.agriculturalperiods_periodid_seq OWNED BY public.agriculturalperiods.periodid;
          public          postgres    false    217            �            1259    16797    crops    TABLE     i   CREATE TABLE public.crops (
    cropid integer NOT NULL,
    cropname character varying(255) NOT NULL
);
    DROP TABLE public.crops;
       public         heap    postgres    false            �            1259    16796    crops_cropid_seq    SEQUENCE     �   CREATE SEQUENCE public.crops_cropid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.crops_cropid_seq;
       public          postgres    false    216            �           0    0    crops_cropid_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.crops_cropid_seq OWNED BY public.crops.cropid;
          public          postgres    false    215            �            1259    16811    suggestions    TABLE     �   CREATE TABLE public.suggestions (
    suggestionid integer NOT NULL,
    cropid integer,
    periodid integer,
    proposal text
);
    DROP TABLE public.suggestions;
       public         heap    postgres    false            �            1259    16810    suggestions_suggestionid_seq    SEQUENCE     �   CREATE SEQUENCE public.suggestions_suggestionid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.suggestions_suggestionid_seq;
       public          postgres    false    220            �           0    0    suggestions_suggestionid_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.suggestions_suggestionid_seq OWNED BY public.suggestions.suggestionid;
          public          postgres    false    219            %           2604    16807    agriculturalperiods periodid    DEFAULT     �   ALTER TABLE ONLY public.agriculturalperiods ALTER COLUMN periodid SET DEFAULT nextval('public.agriculturalperiods_periodid_seq'::regclass);
 K   ALTER TABLE public.agriculturalperiods ALTER COLUMN periodid DROP DEFAULT;
       public          postgres    false    218    217    218            $           2604    16800    crops cropid    DEFAULT     l   ALTER TABLE ONLY public.crops ALTER COLUMN cropid SET DEFAULT nextval('public.crops_cropid_seq'::regclass);
 ;   ALTER TABLE public.crops ALTER COLUMN cropid DROP DEFAULT;
       public          postgres    false    216    215    216            &           2604    16814    suggestions suggestionid    DEFAULT     �   ALTER TABLE ONLY public.suggestions ALTER COLUMN suggestionid SET DEFAULT nextval('public.suggestions_suggestionid_seq'::regclass);
 G   ALTER TABLE public.suggestions ALTER COLUMN suggestionid DROP DEFAULT;
       public          postgres    false    220    219    220            �          0    16804    agriculturalperiods 
   TABLE DATA           W   COPY public.agriculturalperiods (periodid, periodname, startdate, enddate) FROM stdin;
    public          postgres    false    218   �!       �          0    16797    crops 
   TABLE DATA           1   COPY public.crops (cropid, cropname) FROM stdin;
    public          postgres    false    216   �"       �          0    16811    suggestions 
   TABLE DATA           O   COPY public.suggestions (suggestionid, cropid, periodid, proposal) FROM stdin;
    public          postgres    false    220   �"       �           0    0     agriculturalperiods_periodid_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.agriculturalperiods_periodid_seq', 9, true);
          public          postgres    false    217            �           0    0    crops_cropid_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.crops_cropid_seq', 4, true);
          public          postgres    false    215            �           0    0    suggestions_suggestionid_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.suggestions_suggestionid_seq', 13, true);
          public          postgres    false    219            *           2606    16809 ,   agriculturalperiods agriculturalperiods_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.agriculturalperiods
    ADD CONSTRAINT agriculturalperiods_pkey PRIMARY KEY (periodid);
 V   ALTER TABLE ONLY public.agriculturalperiods DROP CONSTRAINT agriculturalperiods_pkey;
       public            postgres    false    218            (           2606    16802    crops crops_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.crops
    ADD CONSTRAINT crops_pkey PRIMARY KEY (cropid);
 :   ALTER TABLE ONLY public.crops DROP CONSTRAINT crops_pkey;
       public            postgres    false    216            ,           2606    16818    suggestions suggestions_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.suggestions
    ADD CONSTRAINT suggestions_pkey PRIMARY KEY (suggestionid);
 F   ALTER TABLE ONLY public.suggestions DROP CONSTRAINT suggestions_pkey;
       public            postgres    false    220            -           2606    16819 #   suggestions suggestions_cropid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.suggestions
    ADD CONSTRAINT suggestions_cropid_fkey FOREIGN KEY (cropid) REFERENCES public.crops(cropid);
 M   ALTER TABLE ONLY public.suggestions DROP CONSTRAINT suggestions_cropid_fkey;
       public          postgres    false    216    4648    220            .           2606    16829 $   suggestions suggestions_cropid_fkey1    FK CONSTRAINT     �   ALTER TABLE ONLY public.suggestions
    ADD CONSTRAINT suggestions_cropid_fkey1 FOREIGN KEY (cropid) REFERENCES public.crops(cropid);
 N   ALTER TABLE ONLY public.suggestions DROP CONSTRAINT suggestions_cropid_fkey1;
       public          postgres    false    220    4648    216            /           2606    16824 %   suggestions suggestions_periodid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.suggestions
    ADD CONSTRAINT suggestions_periodid_fkey FOREIGN KEY (periodid) REFERENCES public.agriculturalperiods(periodid);
 O   ALTER TABLE ONLY public.suggestions DROP CONSTRAINT suggestions_periodid_fkey;
       public          postgres    false    218    4650    220            0           2606    16834 &   suggestions suggestions_periodid_fkey1    FK CONSTRAINT     �   ALTER TABLE ONLY public.suggestions
    ADD CONSTRAINT suggestions_periodid_fkey1 FOREIGN KEY (periodid) REFERENCES public.agriculturalperiods(periodid);
 P   ALTER TABLE ONLY public.suggestions DROP CONSTRAINT suggestions_periodid_fkey1;
       public          postgres    false    218    220    4650            �   �   x�u�m
�0�7���~l�vO#���B��)�8A�M�ۘn�Up4��}�4Z���O7�n�|}����H�̤�R[0/j�ʲ�Ɂ#�񉗤و�8���p�INu�"�To�FM4ё��x��F%,�X�5�&���VLxe��/�V�"a���{X5Q�*��J��'��ե]�����&��      �   =   x�3伱�fˍM7�n���q���"��f�� ��"���v����\&`�������� (�      �     x�͒Mn� ��p��uSUu��)�t3�8	 �q��9|�EU6]XYe���xO�:թ�ʌ,_0Z�H�Y��0�����ep6�'�7g�́����G��f���DF��.�zc��D�īWG9�{����)����).�I�2�l�t��[��n��%�}�
�G�}Q�V�U췡o`#�=��V���c�.�?�1ө�_�	s�S��s�3�i����I,�Z�IpO�L��^���u���w��@)a+�5��j��*P��{
���kd�     