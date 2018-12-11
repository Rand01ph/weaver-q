local task_id = ARGV[1];
local task_dill = ARGV[2];

local task_data_key = KEYS[1];
local task_done_key = KEYS[2]
local tid_list_key = KEYS[3];

local state = nil;

if redis.call('hexists', task_data_key, task_id) == 1 then
    if redis.call('sismember', task_done_key, task_id) == 1 then
	state = 'done-awaiting-gc';
    else
	state = 'queued';
    end
end


if state == 'done-awaiting-gc' then
    -- 处理数据
    redis.call('srem', task_done_key, task_id);
    return task_id;
end


if state == nil then
    redis.call('hset', task_data_key, task_id, task_dill);

    if redis.call('exists', tid_list_key, task_id) ~= 1 then
	redis.call('lpush', tid_list_key, 'end-of-circle');
    end

    redis.call('lpush', tid_list_key, task_id);
else
    return state;
end

return task_id;
