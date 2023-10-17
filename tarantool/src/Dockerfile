FROM tarantool/tarantool:latest

COPY *.lua /opt/tarantool/
EXPOSE 3302
WORKDIR /opt/tarantool

CMD ["tarantool", "init.lua"]