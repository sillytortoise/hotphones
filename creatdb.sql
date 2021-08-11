use hotphones;
create table newphones(
	id int unsigned auto_increment,
    pname varchar(50),
    os varchar(50),
    ptype varchar(50),
    brand varchar(20),
    size float,
    resolution char(9),
    pcpu varchar(50),
    screen varchar(20),
    link varchar(100),
    img varchar(255),
    primary key(id,pname)
);