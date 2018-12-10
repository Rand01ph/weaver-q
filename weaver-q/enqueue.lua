local task_id = ARGV[1];
local task_dill = ARGV[2];

redis.call('hset', KEYS[1], task_id, task_dill);

if redis.call('exists', KEYS[4], task_id) ~= 1 then
    redis.call('lpush', KEYS[4], 'end-of-circle');
end

redis.call('lpush', KEYS[4], task_id);

return task_id;
