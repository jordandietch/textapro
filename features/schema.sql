drop table if exists entries;
create table leads (
  id integer primary key autoincrement,
  telephone string not null,
  received_on date not null
);