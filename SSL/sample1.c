/*
 * User controllable parameters are:
 * - `const char __user *buf`
 * - `size_t count`
*/
static ssize_t proc_pid_attr_write(struct file * file, const char __user * buf,
                                   size_t count, loff_t *ppos)
{
        struct inode * inode = file_inode(file);
        void *page;
        ssize_t length;
        struct task_struct *task = get_proc_task(inode);

        length = -ESRCH;
        if (!task)
                goto out_no_task;
        if (count > PAGE_SIZE)
                count = PAGE_SIZE;

        /* No partial writes. */
        length = -EINVAL;
        if (*ppos != 0)
                goto out;

        // This function is simillar as `malloc()`
        page = memdup_user(buf, count);
        if (IS_ERR(page)) {
                length = PTR_ERR(page);
                goto out;
        }

        /* Guard against adverse ptrace interaction */
        length = mutex_lock_interruptible(&task->signal->cred_guard_mutex);
        if (length < 0)
                goto out_free;

        // This function calls `apparmor_setprocattr()`
        length = security_setprocattr(task,
                                      (char*)file->f_path.dentry->d_name.name,
                                      page, count);
...

static int apparmor_setprocattr(struct task_struct *task, char *name,
                                void *value, size_t size)
{
        struct common_audit_data sa;
        struct apparmor_audit_data aad = {0,};
        char *command, *args = value;
        size_t arg_size;
        int error;

        if (size == 0)
                return -EINVAL;
        /* args points to a PAGE_SIZE buffer, AppArmor requires that
         * the buffer must be null terminated or have size <= PAGE_SIZE -1
         * so that AppArmor can null terminate them
         */
        if (args[size - 1] != '\0') {
                if (size == PAGE_SIZE)
                        return -EINVAL;
                args[size] = '\0';
        }
...