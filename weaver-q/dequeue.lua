-- RPOPLPUSH # move the job from the head to tail within the same list, return <task id>
-- HGET # fetch the job payload

local task_id = redis.call('rpoplpush', KEYS[2], KEYS[2]);

local task_dill = redis.call('hget', KEYS[1], task_id)

return {task_id, task_dill};
