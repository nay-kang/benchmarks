import sqlite3
from sqlite3 import Cursor
import os
import string
import random
from timeit import timeit
import hashlib
import argparse



def prepare_db():
    db_path = '/tmp/test_db.sq3'
    if os.path.exists(db_path):
        os.unlink(db_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    return cur

def get_random_str(len):
    chars = string.ascii_letters + string.digits
    random_string = "".join([random.choice(chars) for _ in range(len)])
    return random_string

def prepare_table_direct(cur:Cursor,size:int):
    cur.execute('''
    create table tbl(
        id integer primary key,
        content text
        );
                ''')
    cur.connection.commit()
    for i in range(size):
        content = get_random_str(TEXT_LEN)
        cur.execute(f'''
            insert into tbl(content) values("{content}");
                    ''')
    cur.connection.commit()

def prepare_table_hashed(cur:Cursor,size:int,index=False):
    cur.execute('''
    create table tbl(
        id integer primary key,
        content text,
        hash text
        );
                ''')
    if index:
        cur.execute('''
            create index hash_idx on tbl (hash);
                    ''')
    cur.connection.commit()
    for i in range(size):
        content = get_random_str(TEXT_LEN)
        ct_hash = hashlib.sha3_256(content.encode()).hexdigest()
        cur.execute(f'''
            insert into tbl(content,hash) values("{content}","{ct_hash}");
                    ''')
    cur.connection.commit()

def run_direct(cur:Cursor,size,count,id_filter=False):
    for i in range(count):
        row_id = random.randint(1,size)
        cur.execute(f'select content from tbl where id={row_id}')
        content = cur.fetchone()[0]
        sql = f'select * from tbl where content="{content}"'
        if id_filter:
            sql += f' and id={row_id}'
        cur.execute(sql)
        cur.fetchone()
        
    for i in range(count):
        content = get_random_str(TEXT_LEN)
        sql = f'select * from tbl where content="{content}"'
        if id_filter:
            row_id = random.randint(1,size)
            sql += f' and id={row_id}'
        cur.execute(sql)
        cur.fetchone()

def run_hashed(cur,size,count):
    for i in range(count):
        row_id = random.randint(1,size)
        cur.execute(f'select content from tbl where id={row_id}')
        content = cur.fetchone()[0]
        ct_hash = hashlib.sha3_256(content.encode()).hexdigest()
        cur.execute(f'select * from tbl where hash="{ct_hash}"')
        cur.fetchone()
        
    for i in range(count):
        content = get_random_str(TEXT_LEN)
        ct_hash = hashlib.sha3_256(content.encode()).hexdigest()
        cur.execute(f'select * from tbl where hash="{ct_hash}"')
        cur.fetchone()

if __name__=='__main__':
    parser = argparse.ArgumentParser('text query benchmark')
    parser.add_argument('-text_length',default=999999)
    parser.add_argument('-table_size',default=1000)
    parser.add_argument('-iterate',default=1000)
    args = parser.parse_args()
    size = args.table_size
    count = args.iterate
    TEXT_LEN=args.text_length
    
    cur = prepare_db()
    prepare_t = timeit(lambda: prepare_table_direct(cur,size),number=1)
    run_t = timeit(lambda : run_direct(cur,size,count),number=1)
    print(f"direct prepare:{prepare_t} run:{run_t}")
    
    cur = prepare_db()
    prepare_t = timeit(lambda: prepare_table_direct(cur,size),number=1)
    run_t = timeit(lambda : run_direct(cur,size,count,True),number=1)
    print(f"direct with id filter prepare:{prepare_t} run:{run_t}")
    
    cur = prepare_db()
    prepare_t = timeit(lambda: prepare_table_hashed(cur,size),number=1)
    run_t = timeit(lambda : run_hashed(cur,size,count),number=1)
    print(f"hash prepare:{prepare_t} run:{run_t}")
    
    cur = prepare_db()
    prepare_t = timeit(lambda: prepare_table_hashed(cur,size,True),number=1)
    run_t = timeit(lambda : run_hashed(cur,size,count),number=1)
    print(f"hash with index prepare:{prepare_t} run:{run_t}")
    