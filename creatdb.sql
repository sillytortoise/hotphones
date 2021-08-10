use hotphones;
create table phones(
	id int unsigned auto_increment,
    pname varchar(50),
    os char(20),
    ptype varchar(50),
    brand varchar(20),
    size float,
    resolution char(9),
    pcpu varchar(50),
    screen varchar(20),
    primary key(id,pname)
)