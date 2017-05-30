# A test load balancer (v1) with all the network resources created
# created from scratch and test instances as members.
# https://www.terraform.io/docs/providers/openstack/r/lb_pool_v1.html

resource "openstack_networking_network_v2" "network_1" {
  name           = "network_1"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "subnet_1" {
  network_id = "${openstack_networking_network_v2.network_1.id}"
  cidr       = "192.168.199.0/24"
  ip_version = 4
}

resource "openstack_compute_secgroup_v2" "secgroup_1" {
  name        = "secgroup_1"
  description = "Rules for secgroup_1"

  rule {
    from_port   = -1
    to_port     = -1
    ip_protocol = "icmp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

resource "openstack_compute_instance_v2" "instance_1" {
  name            = "instance_1"
  security_groups = ["default", "${openstack_compute_secgroup_v2.secgroup_1.name}"]

  network {
    uuid = "${openstack_networking_network_v2.network_1.id}"
  }
}

resource "openstack_compute_instance_v2" "instance_2" {
  name            = "instance_2"
  security_groups = ["default", "${openstack_compute_secgroup_v2.secgroup_1.name}"]

  network {
    uuid = "${openstack_networking_network_v2.network_1.id}"
  }
}

resource "openstack_lb_monitor_v1" "monitor_1" {
  type           = "TCP"
  delay          = 30
  timeout        = 5
  max_retries    = 3
  admin_state_up = "true"
}

resource "openstack_lb_pool_v1" "pool_1" {
  name        = "pool_1"
  protocol    = "TCP"
  subnet_id   = "${openstack_networking_subnet_v2.subnet_1.id}"
  lb_method   = "ROUND_ROBIN"
  monitor_ids = ["${openstack_lb_monitor_v1.monitor_1.id}"]
}

resource "openstack_lb_member_v1" "member_1" {
  pool_id = "${openstack_lb_pool_v1.pool_1.id}"
  address = "${openstack_compute_instance_v2.instance_1.access_ip_v4}"
  port    = 80
}

resource "openstack_lb_member_v1" "member_2" {
  pool_id = "${openstack_lb_pool_v1.pool_1.id}"
  address = "${openstack_compute_instance_v2.instance_2.access_ip_v4}"
  port    = 80
}

resource "openstack_lb_vip_v1" "vip_1" {
  name      = "vip_1"
  subnet_id = "${openstack_networking_subnet_v2.subnet_1.id}"
  protocol  = "TCP"
  port      = 80
  pool_id   = "${openstack_lb_pool_v1.pool_1.id}"
}

# A floating IP
resource "openstack_networking_floatingip_v2" "floatip_1" {
  pool = "external"
}

# A test volume
resource "openstack_blockstorage_volume_v1" "testvol" {
  name     = "testvol"
  description = "A test volume"
  size     = 2
}

# A test image
resource "openstack_images_image_v2" "rancheros" {
  name   = "RancherOS"
  image_source_url = "https://releases.rancher.com/os/latest/rancheros-openstack.img"
  container_format = "bare"
  disk_format = "qcow2"
}

# FWaaS (v1)
# https://www.terraform.io/docs/providers/openstack/r/fw_firewall_v1.html
resource "openstack_fw_rule_v1" "rule_1" {
  name             = "my-rule-1"
  description      = "drop TELNET traffic"
  action           = "deny"
  protocol         = "tcp"
  destination_port = "23"
  enabled          = "true"
}

resource "openstack_fw_rule_v1" "rule_2" {
  name             = "my-rule-2"
  description      = "drop NTP traffic"
  action           = "deny"
  protocol         = "udp"
  destination_port = "123"
  enabled          = "false"
}

resource "openstack_fw_policy_v1" "policy_1" {
  name = "my-policy"

  rules = ["${openstack_fw_rule_v1.rule_1.id}",
    "${openstack_fw_rule_v1.rule_2.id}",
  ]
}

resource "openstack_fw_firewall_v1" "firewall_1" {
  name      = "my-firewall"
  policy_id = "${openstack_fw_policy_v1.policy_1.id}"
}

